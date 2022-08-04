import hashlib
import json
import os.path

from PySide2 import QtCore

from opencmiss.merger.points import Merger, display_field_info


class MarkerMapModel(QtCore.QAbstractTableModel):

    def __init__(self, target_info, source_info, marker_indices=None, parent=None):
        super(MarkerMapModel, self).__init__(parent)
        self._headers = ['Target Marker', 'Source Marker']
        self._target_info = target_info
        self._source_info = source_info
        self._source_indices = [-1] * len(target_info)
        if marker_indices is None:
            self._preliminary_match_source_index()
        else:
            self._source_indices = marker_indices
        self._row_count = len(target_info)

    def get_source_indices(self):
        return self._source_indices

    def get_marker_information(self, row):
        if self._source_indices[row] == -1:
            return None, None

        return self._target_info[row], self._source_info[self._source_indices[row]]

    def _get_matching_source_info_index(self, name):
        matching_source_index = [i for i, s in enumerate(self._source_info) if s["name"] == name]
        if len(matching_source_index):
            return matching_source_index[0]

        return -1

    def _preliminary_match_source_index(self):
        for index in range(len(self._target_info)):
            target_name = self._target_info[index]["name"]
            self._source_indices[index] = self._get_matching_source_info_index(target_name)

    def columnCount(self, parent) -> int:
        return 2

    def rowCount(self, parent) -> int:
        return self._row_count

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            if index.column() == 0:
                return self._target_info[row]["name"]
            elif index.column() == 1:
                if row >= len(self._source_indices) or self._source_indices[row] == -1:
                    return "--"
                return self._source_info[self._source_indices[row]]["name"]

            return "--"
        elif role == QtCore.Qt.EditRole:
            if index.column() == 1:
                values = ["--"]
                values.extend([s["name"] for s in self._source_info])
                return values
        elif role == QtCore.Qt.ToolTipRole:
            text = ["Marker field information\n"]
            if index.column() == 0:
                marker_info = self._target_info[index.row()]
                text.extend([display_field_info(f) for f in marker_info["fields"]])
            elif index.column() == 1:
                source_index = self._source_indices[index.row()]
                if source_index == -1:
                    return None
                else:
                    marker_info = self._source_info[source_index]
                    text.extend([display_field_info(f) for f in marker_info["fields"]])

            return "\n".join(text)

        return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._headers[section]

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                self._source_indices[index.row()] = self._get_matching_source_info_index(value)
                self.dataChanged.emit(index, index)
                return True

        return False

    def flags(self, index):
        if index.isValid():
            if index.column() == 1:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.NoItemFlags


class MergeZincDataModel(object):

    def __init__(self, settings):
        self._dominant_file = settings["dominant_file"]
        self._recessive_file = settings["recessive_file"]
        self._location = settings["location"]
        self._identifier = settings["identifier"]

        settings_dir = os.path.join(self._location, self._identifier + "-settings")
        if not os.path.isdir(settings_dir):
            os.mkdir(settings_dir)

        filename_parts = os.path.splitext(os.path.basename(self._dominant_file))
        self._output_file = os.path.join(settings_dir, filename_parts[0] + "_merged.exf")

        self._merger = Merger()
        self._merger.load_dominant_data(self._dominant_file)
        self._merger.load_recessive_data(self._recessive_file)

        target_info = self._merger.fetch_marker_information("dominant")
        source_info = self._merger.fetch_marker_information("recessive")

        text = json.dumps(target_info)
        text += json.dumps(source_info)
        hex_value = hashlib.sha1(text.encode("utf-8")).hexdigest()

        self._indices_file = os.path.join(settings_dir, f'settings-{hex_value}.json')
        marker_indices = None
        if os.path.isfile(self._indices_file):
            with open(self._indices_file) as f:
                marker_indices = json.load(f)

        self._marker_model = MarkerMapModel(target_info, source_info, marker_indices)

    def get_marker_model(self):
        return self._marker_model

    def get_merged_data_file(self):
        return self._output_file

    def done(self):
        with open(self._indices_file, "w") as f:
            json.dump(self._marker_model.get_source_indices(), f)

        # clone_items = []
        for row in range(self._marker_model.rowCount(None)):
            dominant_marker_information, recessive_marker_information = self._marker_model.get_marker_information(row)
            if dominant_marker_information is not None and recessive_marker_information is not None:
                dominant_item = {
                    "node": self._get_marker_information_node("dominant", dominant_marker_information),
                    "info": dominant_marker_information
                }
                recessive_item = {
                    "node": self._get_marker_information_node("recessive", recessive_marker_information),
                    "info": recessive_marker_information
                }
                self._merger.merge(dominant_item, recessive_item)
                # clone_items.append(dominant_item)

        # self._merger.clone(clone_items)
        self._merger.get_dominant_region().writeFile(self._output_file)

    def _get_marker_information_node(self, kind, marker_information):
        if kind == "dominant":
            field_module = self._merger.get_dominant_region().getFieldmodule()
        elif kind == "recessive":
            field_module = self._merger.get_recessive_region().getFieldmodule()
        else:
            return None

        domain_nodes = field_module.findNodesetByFieldDomainType(marker_information["domain"])
        return domain_nodes.findNodeByIdentifier(marker_information["id"])

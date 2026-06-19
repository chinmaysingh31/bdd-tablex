from bdd_tablex import ColumnTable, field, id_field


class ContentTable(ColumnTable):
    id = id_field("IDs")
    headline = field("Headline*", required=True)
    status = field("Status")

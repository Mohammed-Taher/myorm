class Model:
    db = None
    connection = None

    def __init__(self):
        self._create_tables()
        self._saved = False

    @classmethod
    def all(cls):
        results = []
        sql = f'SELECT * FROM {cls.get_table_name()}'
        records = cls.connection.execute(sql)
        return records.fetchall()

    @classmethod
    def get(cls, id):
        sql = f'SELECT * FROM {cls.get_table_name()} WHERE id = {id}'
        result = cls.connection.execute(sql)
        row = result.fetchone()
        return row

    @classmethod
    def find(cls, col_name, operator, value):
        if operator == 'LIKE':
            value = '%' + value + '%'
        sql = f'SELECT * FROM {cls.get_table_name()} WHERE {col_name} {operator} "{value}"'
        print(sql)
        records = cls.connection.execute(sql)
        results = records.fetchall()
        return results

    def has(self, id):
        sql = f'SELECT * FROM {self.get_table_name()} WHERE id = {id}'
        record = self.connection.execute(sql)
        return True if record.fetchall() else False

    def save(self):
        if self._saved:
            self._update()
            return
        fields = []
        values = []
        for key, value in self.get_values().items():
            fields.append(key)
            values.append(f"'{value}'")

        sql = f'INSERT INTO {self.get_table_name()} ({", ".join(fields)}) VALUES ({", ".join(values)})'
        result = self.connection.execute(sql)
        self.connection.commit()
        self._saved = True
        # return result.fetchall()

    def _update(self):
        old = self.find('created_at', '=', self.get_values()['created_at'])
        old_id = old[0][0]
        new_values = []
        for key, value in self.get_values().items():
            new_values.append(f'{key} = "{value}"')

        expression = ', '.join(new_values)

        sql = f'UPDATE {self.get_table_name()} SET {expression} WHERE id = {old_id}'
        print(old)
        print(sql)
        result = self.connection.execute(sql)
        self.connection.commit()


    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_columns(cls):
        columns = {}
        for key, value in cls.__dict__.items():
            if str(key).startswith('_'):
                continue
            columns[str(key)] = str(value)

        return columns

    def get_values(self):
        values = {}
        for key, value in self.__dict__.items():
            if str(key).startswith('_'):
                continue
            if value is False:
                value = 0
            if value is True:
                value = 1
            values[key] = value
        return values

    def _create_tables(self):
        columns = ', '.join(' '.join((key, value)) for (key, value) in self.get_columns().items())
        sql = f'CREATE TABLE IF NOT EXISTS {self.get_table_name()} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})'
        cursor = self.connection.cursor()
        result = cursor.execute(sql)
        return result

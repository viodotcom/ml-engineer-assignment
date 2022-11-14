from abc import ABC
from dataclasses import dataclass
import random
from typing import Optional
import os
import pandas as pd
import datetime
import uuid
import string

from ruamel.yaml import YAML
yaml = YAML(typ='safe')
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.default_flow_style = False


unique_values = [
    str(uuid.uuid4().int)[:10] for _ in range(10000)
]

ROOT_DIR = '.'
with open(os.path.join(ROOT_DIR, 'model_config.yml'), "r") as stream:
    try:
        config = dict(yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)


class DataGen(ABC):
    def generate(self, size: int) -> list:
        raise NotImplementedError()


@dataclass
class STRINGTYPE(DataGen):
    values: Optional[list[str]] = None
    unique: Optional[bool] = None
    length: Optional[int] = None

    def generate(self, size: int) -> list:
        self.size = size
        if self.values is not None:
            return self.__generate_default()
        if self.unique is True:
            return self.__generate_unique()
        if self.length is not None:
            return self.generate_length()
        else:
            return [None] * self.size

    def __generate_unique(self):
        if self.values:
            raise ValueError('values needs be none for unique values')
        return random.sample(unique_values, k=self.size)

    def generate_length(self):
        letters = string.ascii_uppercase
        length_data = [''.join(random.choice(letters) for _ in range(self.length)) for _ in range(self.size+1)]
        return random.sample(length_data, k=self.size)

    def __generate_default(self):
        column_values = self.values * self.size
        random.shuffle(column_values)
        return random.sample(column_values, k=self.size)


@dataclass
class INTEGERTYPE(DataGen):
    min: Optional[int] = None
    max: Optional[int] = None
    mean: Optional[int] = None
    std: Optional[int] = None
    calculated: Optional[bool] = None
    calculated_columns: Optional[list[str]] = None
    calcluated_type: Optional[str] = None

    def generate(self, size: int) -> list:
        self.size = size
        if self.calculated is True:
            # We need to leave the computation to the end of the data generation
            return self.generate_calculated()
        return self.generate_default()

    def generate_calculated(self):
        return [None] * self.size

    def generate_default(self):
        return [None] * self.size


@dataclass
class DATETIMETYPE(DataGen):
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    unique: Optional[bool] = None

    def generate(self, size: int) -> list:
        self.size = size
        return self.__generate_default()

    def __generate_default(self):
        # get data difference
        from_date = datetime.datetime.strptime(self.from_date, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(self.to_date, '%Y-%m-%d')

        diff = to_date - from_date

        # generate list of date between from_date and to_date
        date_list = [
            from_date + datetime.timedelta(
                days=random.randrange(diff.days)
            ) for _ in range(self.size)
        ]
        # sample the date to the size of data
        return date_list


def data_gen(config, *, size=100):
    """
    Generate training data for the model.
    """
    if 'features' in config:
        features = config['features']
        assert len(features) > 0, 'No features specified'

        for feature in features:
            source_file = os.path.join(ROOT_DIR, feature['source'])

            source_data = {}
            date_colums = []
            date_values = []
            columns = feature['columns']
            assert len(columns) > 0, 'No columns specified'

            for column in columns:
                if column['type'] == 'string':
                    source_data[column['name']] = STRINGTYPE(
                        **column['xteristics']
                    ).generate(size=size)
                elif column['type'] == 'integer':
                    source_data[column['name']] = INTEGERTYPE(
                        **column['xteristics']
                    ).generate(size=size)

                elif column['type'] == 'datetime':
                    date_colums.append(column['name'])
                    date_values.append(DATETIMETYPE(
                        **column['xteristics']
                    ).generate(size=size))
                else:
                    raise ValueError('Invalid column type')

            # Sort the date values in ascending order column wise
            transposed = list(zip(*date_values))
            tmp = [sorted(x) for x in transposed]
            final_dates = list(zip(*tmp))
            for i in range(len(date_colums)):
                source_data[date_colums[i]] = final_dates[i]

            source_data = pd.DataFrame(source_data)

            if 'check_out' in source_data.columns and 'check_in' in source_data.columns:
                source_data['length_of_stay'] = (source_data['check_out'] - source_data['check_in']).dt.days

            if 'date' in source_data.columns and 'check_in' in source_data.columns:
                source_data['day_distance'] = (source_data['check_in'] - source_data['date'] ).dt.days

            source_data.to_csv(
                source_file,
                index=False
            )
            assert os.stat(source_file) != 0, 'Source file is empty'
    return


def train_data_gen(config, *, size=100):
    """
    Generate training data for the model.
    """
    return data_gen(config=config, size=size)


if __name__ == '__main__':
    train_data_gen(config)
    print(config)

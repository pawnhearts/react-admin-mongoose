from fire import Fire
import re
from collections import defaultdict


type_map = defaultdict(lambda: 'TextInput')
type_map.update({'String': 'TextInput', 'Number': 'NumberInput', 'Boolean': 'BooleanInput', 'Date': 'DateInput'})

tpl = '''
import * as React from "react";
import {
  List,
  Datagrid,
  Edit,
  Create,
  SimpleForm,
  DateField,
  TextField,
  EditButton,
  DeleteButton,
  TextInput,
  NumberInput,
  BooleanInput,
  DateInput,
} from "react-admin";
import BookIcon from "@material-ui/icons/Book";
export const %(name)sIcon = BookIcon;

export const %(name)sList = (props) => (
  <List {...props}>
    <Datagrid>
      <TextField source="id" />
      <EditButton basePath="/%(url)s" />
    </Datagrid>
  </List>
);

const %(name)sTitle = ({ record }) => {
  return <span>%(name)s {record ? `"${record.title}"` : ""}</span>;
};

export const %(name)sEdit = (props) => (
  <Edit title={<%(name)sTitle />} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
       %(form)s
    </SimpleForm>
  </Edit>
);

export const %(name)sCreate = (props) => (
  <Create title="Create a %(name)s" {...props}>
    <SimpleForm>
        %(form)s
    </SimpleForm>
  </Create>
);
// import { %(name)sList, %(name)sEdit, %(name)sCreate, %(name)sIcon } from "./%(url)s";
// <Resource name="%(url)s" list={%(name)sList}  edit={%(name)sEdit} create={%(name)sCreate} icon={%(name)sIcon} />

'''

def to_fields(data):
    for name, typ in data:
        if name == 'timestamps':
            yield '<DateField source="createdAt" />'
        else:
            yield f'<{type_map[typ]} source="{name}" />'

def main(model):
    model = open(model).read()
    name = re.search('''model\(['"](\w+)['"]''', model).groups(0)[0]
    url = f'{name.lower()}s'
    schema = model.split('Schema(', 1)[1].split(')', 1)[0]
    form = '\n'.join(to_fields(re.findall('([\w\d_]+):\s?(\S+),', schema)))
    print(tpl % {'name': name, 'url': url, 'form': form})

if __name__ == '__main__':
    Fire(main)


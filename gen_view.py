from fire import Fire
import re
import demjson
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
        if isinstance(typ, dict):
            typ = typ.get('type', None)
        if typ is None:
            continue
        yield f'      <{type_map[typ]} source="{name}" />'


def strip_obj(text):
    count = 1
    res = '{'
    in_quotes = False

    for s in text[1:]:
        if not in_quotes and s == '{':
            count += 1
        elif  not in_quotes and s == '}':
            count -= 1
        for quote in '\'"':
            if s == quote:
                in_quotes = False if in_quotes == quote else quote
        res += s
        if not count:
            break
    return res
        


def main(model):
    model = open(model).read()
    name = re.search('''model\(['"](\w+)['"]''', model).groups(0)[0]
    url = f'{name.lower()}s'
    schema = model.split('Schema(', 1)[1].split(')', 1)[0]
    for k in type_map:
        schema = schema.replace(k, f'"{k}"')
    timestamps = 'timestamps' in schema
    schema = strip_obj(schema)
    schema = demjson.decode(schema)
    if timestamps:
        schema['createdAt'] = 'Date'
    form = '\n'.join(to_fields(schema.items()))
    #form = '\n'.join(to_fields(re.findall('([\w\d_]+):\s?(\S+),', schema)))
    print(tpl % {'name': name, 'url': url, 'form': form})

if __name__ == '__main__':
    Fire(main)


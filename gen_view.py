from fire import Fire

type_map = {'String': 'TextInput', 'Number': 'NumberInput', 'Boolean': 'BooleanInput'}

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
export const {name}Icon = BookIcon;

export const {name}List = (props) => (
  <List {...props}>
    <Datagrid>
      <TextField source="id" />
      <EditButton basePath="/{url}" />
    </Datagrid>
  </List>
);

const {name}Title = ({ record }) => {
  return <span>{name} {record ? `"${record.title}"` : ""}</span>;
};

export const {name}Edit = (props) => (
  <Edit title={<{name}Title />} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
       {form}
    </SimpleForm>
  </Edit>
);

export const {name}Create = (props) => (
  <Create title="Create a {name}" {...props}>
    <SimpleForm>
        {form}
    </SimpleForm>
  </Create>
);
// import { {name}List, {name}Edit, {name}Create, {name}Icon } from "./{url}";
// <Resource name="{url}" list={{name}List}  edit={{name}Edit} create={{name}Create} icon={{name}Icon} />

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
    print(tpl.format(name=name, url=url, form=form))

if __name__ == '__main__':
    fire.Fire(main)


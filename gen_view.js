const schema = require(process.argv[1]).schema;
const model = require(process.argv[1]).model;

const type_map = {
  String: "TextInput",
  Number: "NumberInput",
  Boolean: "BooleanInput",
  Date: "DateInput",
};

let form = Object.keys(schema.paths)
  .map((k) => {
    return `      <${type_map[schema.paths[k].instance]} source="${k}" />`;
  })
  .join("\n");

let url = model.collection.name;
let name = model.modelName;

console.log(`import * as React from "react";`);
console.log(`import {`);
console.log(`  List,`);
console.log(`  Datagrid,`);
console.log(`  Edit,`);
console.log(`  Create,`);
console.log(`  SimpleForm,`);
console.log(`  DateField,`);
console.log(`  TextField,`);
console.log(`  EditButton,`);
console.log(`  DeleteButton,`);
console.log(`  TextInput,`);
console.log(`  NumberInput,`);
console.log(`  BooleanInput,`);
console.log(`  DateInput,`);
console.log(`} from "react-admin";`);
console.log(`import BookIcon from "@material-ui/icons/Book";`);
console.log(`export const ${name}Icon = BookIcon;`);
console.log(`const ${name}Filters = [`);
console.log(`    ${filters}`);
console.log(`];`);
console.log(`export const ${name}List = (props) => (`);
console.log(`  <List {...props} filters={${name}Filters}>`);
console.log(`    <Datagrid>`);
console.log(`      <TextField source="id" />`);
console.log(`      <EditButton basePath="/${url}" />`);
console.log(`    </Datagrid>`);
console.log(`  </List>`);
console.log(`);`);
console.log(`const ${name}Title = ({ record }) => {`);
console.log(
  "  return <span>" + name + ' {record ? `"${record.title}"` : ""}</span>;'
);
console.log(`};`);
console.log(`export const ${name}Edit = (props) => (`);
console.log(`  <Edit title={<${name}Title />} {...props}>`);
console.log(`    <SimpleForm>`);
console.log(`      <TextInput disabled source="id" />`);
console.log(`${form}`);
console.log(`    </SimpleForm>`);
console.log(`  </Edit>`);
console.log(`);`);
console.log(`export const ${name}Create = (props) => (`);
console.log(`  <Create title="Create a ${name}" {...props}>`);
console.log(`    <SimpleForm>`);
console.log(`${form}`);
console.log(`    </SimpleForm>`);
console.log(`  </Create>`);
console.log(`);`);
console.log(
  `// import { ${name}List, ${name}Edit, ${name}Create, ${name}Icon } from "./${url}";`
);
console.log(
  `// <Resource name="${url}" list={${name}List}  edit={${name}Edit} create={${name}Create} icon={${name}Icon} />`
);

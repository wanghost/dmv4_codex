-- 核心领域模型（PostgreSQL）

create table iam_user (
  id bigserial primary key,
  ehr_no varchar(64) unique not null,
  name varchar(128) not null,
  email varchar(256),
  status varchar(32) not null default 'ACTIVE',
  created_at timestamp not null default now()
);

create table iam_role (
  id bigserial primary key,
  code varchar(64) unique not null,
  name varchar(128) not null
);

create table iam_user_role (
  user_id bigint not null references iam_user(id),
  role_id bigint not null references iam_role(id),
  primary key (user_id, role_id)
);

create table data_source (
  id bigserial primary key,
  name varchar(128) unique not null,
  type varchar(32) not null,
  host varchar(256),
  port int,
  db_name varchar(128),
  username varchar(128),
  password_cipher text,
  extra_config jsonb,
  locked boolean not null default false,
  status varchar(32) not null default 'ACTIVE',
  created_by bigint references iam_user(id),
  created_at timestamp not null default now(),
  updated_at timestamp not null default now()
);

create table metadata_table (
  id bigserial primary key,
  datasource_id bigint not null references data_source(id),
  schema_name varchar(128),
  table_name varchar(256) not null,
  chinese_comment varchar(512) not null,
  asset_category varchar(128) not null,
  security_level varchar(32) not null,
  owner_user_id bigint not null references iam_user(id),
  table_status varchar(32) not null,
  layer_code varchar(16) not null,
  ddl_sql text,
  created_at timestamp not null default now(),
  updated_at timestamp not null default now(),
  unique(datasource_id, schema_name, table_name)
);

create table metadata_column (
  id bigserial primary key,
  table_id bigint not null references metadata_table(id) on delete cascade,
  column_name varchar(256) not null,
  data_type varchar(128) not null,
  nullable boolean not null default true,
  chinese_comment varchar(512) not null,
  security_level varchar(32),
  ordinal_position int not null,
  unique(table_id, column_name)
);

create table table_change_log (
  id bigserial primary key,
  table_id bigint not null references metadata_table(id),
  action varchar(32) not null,
  before_snapshot jsonb,
  after_snapshot jsonb,
  operator_user_id bigint not null references iam_user(id),
  ticket_no varchar(128),
  created_at timestamp not null default now()
);

create table standard_head_office_field (
  id bigserial primary key,
  interface_code varchar(128) not null,
  field_name varchar(256) not null,
  field_comment varchar(512),
  security_level varchar(32) not null,
  data_type varchar(128),
  unique(interface_code, field_name)
);

create table standard_branch_ods_field (
  id bigserial primary key,
  branch_code varchar(32) not null,
  table_name varchar(256) not null,
  field_name varchar(256) not null,
  field_comment varchar(512),
  data_type varchar(128),
  unique(branch_code, table_name, field_name)
);

create table standard_mapping (
  id bigserial primary key,
  branch_field_id bigint not null references standard_branch_ods_field(id) on delete cascade,
  ho_field_id bigint not null references standard_head_office_field(id),
  mapping_type varchar(32) not null,
  confidence numeric(5,4),
  confirmed_by bigint references iam_user(id),
  confirmed_at timestamp
);

create table query_export_approval (
  id bigserial primary key,
  applicant_user_id bigint not null references iam_user(id),
  approver_user_id bigint references iam_user(id),
  sql_text text not null,
  reason varchar(1024),
  status varchar(32) not null,
  encrypted_file_uri text,
  created_at timestamp not null default now(),
  approved_at timestamp
);

create table audit_log (
  id bigserial primary key,
  module varchar(64) not null,
  action varchar(64) not null,
  object_type varchar(64),
  object_id varchar(128),
  operator_user_id bigint,
  operator_ip varchar(64),
  detail jsonb,
  created_at timestamp not null default now()
);

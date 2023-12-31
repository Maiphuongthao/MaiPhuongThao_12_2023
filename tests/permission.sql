INSERT INTO permissions (`department_id`,`ob_name`, `ob_action`, `ob_type`, `ob_field`)
VALUES
    (1,'employee', 'create', 'na', 'all'),
    (1,'employee', 'update', 'all', 'all'),
    (1,'employee', 'delete', 'all', 'na'),
    (1,'contract', 'create', 'na', 'all'),
    (1,'contract', 'update', 'no_signature', 'all'),
    (1,'event', 'update', 'all', 'support_id'),
    (1,'event', 'read_no_support', 'no_support', 'na'),
    (2,'client', 'create', 'na', 'all'),
    (2,'client', 'update', 'owned', 'all'),
    (2,'contract', 'update', 'owned', 'status'),
    (2,'contract', 'read_no_signature', 'no_signature', 'na'),
    (2,'contract', 'read_due_amount', 'due_amount', 'na'),
    (2,'event', 'create', 'na', 'all'),
    (3,'event', 'update', 'owned', 'notes'),
    (3,'event', 'read_owned', 'owned', 'na'),
    (1,'event', 'read_all', 'all', 'na'),
    (2,'event', 'read_all', 'all', 'na'),
    (3,'event', 'read_all', 'all', 'na'),
    (1,'employee', 'read_all', 'all', 'all'),
    (2,'employee', 'read_all', 'all', 'all'),
    (3,'employee', 'read_all', 'all', 'all'),
    (1,'contract', 'read_all', 'all', 'all'),
    (2,'contract', 'read_all', 'all', 'all'),
    (3,'contract', 'read_all', 'all', 'all'),
    (1,'event', 'read_one', 'all', 'all'),
    (2,'event', 'read_one', 'all', 'all'),
    (3,'event', 'read_one', 'all', 'all'),
    (1,'employee', 'read_one', 'all', 'all'),
    (2,'employee', 'read_one', 'all', 'all'),
    (3,'employee', 'read_one', 'all', 'all'),
    (1,'contract', 'read_one', 'all', 'all'),
    (2,'contract', 'read_one', 'all', 'all'),
    (3,'contract', 'read_one', 'all', 'all'),
    (1,'client', 'read_all', 'all', 'all'),
    (2,'client', 'read_all', 'all', 'all'),
    (3,'client', 'read_all', 'all', 'all'),
    (1,'client', 'read_one', 'all', 'all'),
    (2,'client', 'read_one', 'all', 'all'),
    (3,'client', 'read_one', 'all', 'all');
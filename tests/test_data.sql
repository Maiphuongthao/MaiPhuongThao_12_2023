USE epic_events;

INSERT INTO departments (`name`)
VALUES
    ('Gestion'),
    ('Commercial'),
    ('Support');

INSERT INTO permissions (`department_id`,`ob_name`, `ob_action`, `ob_list`, `ob_field`)
VALUES
    ('1','employee', 'create', 'n/a', 'n/a'),
    ('1','employee', 'update', 'all', 'all'),
    ('1','employee', 'delete', 'all', 'n/a'),
    ('1','contract', 'create', 'n/a', 'n/a'),
    ('1','contract', 'update', 'no_signature', 'all'),
    ('1','event', 'update', 'all', 'support_id'),
    ('2','contract', 'update', 'owned', 'all'),
    ('2','client', 'create', 'na', 'na'),
    ('2','client', 'create', 'na', 'na'),
    ('2','client', 'update', 'all', 'all'),

    ('2','event', 'create', 'all', 'all'),
    ('2','event', 'update', 'owned', 'all'),
    ('1','event', 'filter_no_support', 'no_support', 'na'),
    ('2','contract', 'filter_no_signature', 'no_signature', 'na'),
    ('2','contract', 'filter_due_amount', 'due_amount', 'na'),
    ('3','event', 'update', 'owned', 'note'),
    ('3','event', 'filter_owned', 'owned', 'na');


INSERT INTO employees (`first_name`, `last_name`, `email`, `department_id`, `encoded_hash`)
VALUES
    ('albert', 'camus', 'gestion1', 1, '$argon2id$v=19$m=65536,t=3,p=4$YnFFKptVhaYFqldkb7rETw$lFei5iQFlrNwFv11Jf/HSAXwZ16THNo5l2Q2JNcY/ck'),
    ('victor', 'hugo', 'commercial1', 2, '$argon2id$v=19$m=65536,t=3,p=4$/kUTgWrAhFPVdC267akARQ$mwSpL0ue2y6A/83w7DCW4392Mb4wNdLo/3oewooObRA'),
    ('jean-baptiste', 'poquelin', 'support1', 3, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww'),
    ('gestion ', '2', 'gestion2', 1, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww'),
    ('commercial', '2', 'commercial2', 2, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww'),
    ('support', '3', 'support2', 3, '$argon2id$v=19$m=65536,t=3,p=4$8UjK8e2GJL2hC7yRi0GRNg$XtdtCN3GNDUPH3YWBAyqyEXXOvQJfXvCcAmOVOEd3Ww');

INSERT INTO client (`first_name`, `last_name`, `email`, `telephone`, `company_name`, `commercial_id`)
VALUES
    ('premier', 'client', 'mail1', '0666666666', 'company1', 2);

INSERT INTO contracts (`client_id`, `total_amount`, `due_amount`, `status`)
VALUES
    ('1', 56.55, 5.5, 'signed'),
    ('1', 645.66, 645.66, 'to_be_signed'),
    ('1', 35.00, 0.00, 'signed');

INSERT INTO events (`contract_id`, `client_id`, `start_date`, `end_date`, `support_contact_id`, `location`, `attendees_number`, `notes`)
VALUES
    (1, 1, '25/05/2023', '29/09/2023', 3, 'Paris', 50, null),
    (2, 1, '25/05/2023', '29/09/2023', null, 'Paris', 50, null),
    (3, 1, '25/05/2023', '29/09/2023', 3, 'Paris', 50, 'fini');
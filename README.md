#User Authentication
    Login with JWT tokens (Access & Refresh tokens)
    Role-based access control
    Secure password handling

#User Registration
    Register new users with validation
    File Upload & Processing

#Upload CSV files
    Detect & clean missing values
    Remove duplicate entries
    Convert dataset into JSON format


#for role access we have to create a role

     INSERT INTO user_roles (role) 
        VALUES 
            ('Admin'), 
            ('User');


#for create a admin

    INSERT INTO user_master (
            id, username, email, phone_number, full_name, description, address, user_role, 
            employee_id, password, raw_password, is_staff, is_active, is_superuser, is_deleted, 
            is_logged_in, created_by, access_token
        ) VALUES (
            1, 'admin@mailinator.com', 'admin@mailinator.com', '1234567890', 'Admin User', 'Admin Account', 
            '123 Admin Street', 1, 'AD001', 'pbkdf2_sha256$600000$5Ik6F4KcWeX8eSyaodd6dk$ECAoCJEhtS7suy3aYryNIeRRCBD8yhhDthIpvnr25CQ=', 'Password@!', 
            TRUE, TRUE, TRUE, FALSE, FALSE, NULL, NULL
        );
            

# then u can create a user how create by admin 
# and then user can login and upload the file and admin also upload the file           
# AssisementProject

$.validator.addMethod("passwordRules", function(value, element) {

    return this.optional(element) || /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,100}$/.test( value );
}, "* Password must contain one uppercase letter, one lowercase, one digit and be 8-100 characters long");

$.validator.addMethod("postcodeRules", function(value, element) {

    return this.optional(element) || /^[A-Za-z]{1,2}[0-9A-Za-z]{1,2}[ ]?[0-9]?[A-Za-z]{2}$/.test( value );
}, "* Postcode must be a valid postcode");

$.validator.addMethod("accountNumberRules", function(value, element) {
    return this.optional(element) || /^(?=.*\d).{8}$/.test( value );
}, "* Postcode must be a valid postcode");
$.validator.addMethod("sortCodeRules", function(value, element) {
    return this.optional(element) || /^(?=.*\d).{6}$/.test( value );
}, "* Postcode must be a valid postcode");


$(function(){
    $("form[name='RegistrationForm']").validate({
        // CODE GOES HERE
        rules: {
            firstname: "required",
            lastname: "required",
            first_line_of_address: "required",
            second_line_of_address: "required",
            security_question:"required",
            security_answer:"required",
            postcode: {
                required: true,
                postcodeRules: true,
            },
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                passwordRules: true
            }
        },
        messages: {
            firstname: "Please enter your firstname",
            lastname: "Please enter your lastname",
            first_line_of_address: "Please enter the First Line of your address",
            second_line_of_address: "Please enter the Second line of your address",
            security_question:"Please choose a question",
            security_answer:"Please provide an answer",
            postcode:{
                postcodeRules: "Please provide a valid postcode",
            },
            email: {
                required: "Please provide an email address",
                email: "Please enter a valid email address"
            },
            password: {
                required: "Please provide a password",
            },
        },
        errorClass: "is-invalid",
    });
})
$(function(){
    $("form[name='emailChangeForm']").validate({
        rules: {
            new_email: {
                required: true,
                email: true
            },
        },
        messages: {
            new_email: {
                required: "Please provide an email address",
                email: "Please enter a valid email address"
            },
        },
        errorClass: "is-invalid",
    });
})
$(function(){
    $("form[name='changePasswordForm']").validate({
        rules: {
            new_password: {
                required: true,
                passwordRules: true,
            }
        },
        messages: {
            new_password: {
                required: "Please provide a password",
            },
        },
        errorClass: "is-invalid",
    });
})
$(function(){
    $("form[name='LoginForm']").validate({
        // CODE GOES HERE
        rules: {
            firstname: "required",
            lastname: "required",
            security_question:"required",
            security_answer:"required",
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                passwordRules: true
            }
        },
        messages: {
            firstname: "Please enter your firstname",
            lastname: "Please enter your lastname",
            security_question:"Please choose a question",
            security_answer:"Please provide an answer",
            email: {
                required: "Please provide an email address",
                email: "Please enter a valid email address"
            },
            password: {
                required: "Please provide a password",
            },
        },
        errorClass: "is-invalid",
    });
})

$(function(){
    $("form[name='transfer_form']").validate({
        // CODE GOES HERE
        rules: {
            email: {
                required: true,
                email: true,
            },
            account_number:{
                required: true,
                accountNumberRules: true
            },
            sort_code:{
                required: true,
                sortCodeRules: true
            },
            transfer_value:{
                required: true,
                number: true,
            }

        },
        messages: {
            email: {
                required: "Please provide an email address",
                email: "Please enter a valid email address",
            },
            account_number:{
                required: "Please provide the account number",
                accountNumberRules: "Please provide a valid account number in the form xxxxxxxx",
            },
            sort_code:{
                required:"Please provide the sort code",
                sortCodeRules: "Please provide a valid sort code in the form xxxxxx",
            },
            transfer_value:{
                required: "Please provide the transfer value",
                number: "Please provide the transfer value as a number",
            }
        },
        errorClass: "is-invalid",
    });
})
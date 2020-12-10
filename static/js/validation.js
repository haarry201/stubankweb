$.validator.addMethod("passwordRules", function(value, element) {

    return this.optional(element) || /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,100}$/.test( value );
}, "* Password must contain one uppercase letter, one lowercase and one digit");


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
                maxLength: 4,
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
            email: {
                required: "Please provide an email address",
                email: "Please enter a valid email address"
            },
            password: {
                required: "Please provide a password",
            },
        },
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
    });
})
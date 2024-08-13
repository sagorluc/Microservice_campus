// ******************************************************************************
// guestaction-> invite firends form validation
document.addEventListener('DOMContentLoaded', function () {
    // alert('reading form insite invite firends...');
    var form = document.getElementById('myForm');

    function showError(field, errorField, errorMessage) {
      errorField.innerHTML = errorMessage;
      field.classList.add('is-invalid');
    }

    function clearError(field, errorField) {
      errorField.innerHTML = '';
      field.classList.remove('is-invalid');
    }

    function validateName(field, errorField) {
      if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
        var errMsgName = 'Special characters are not allowed except letters.'
        showError(field, errorField, errMsgName);
        return false;
      } else {
        clearError(field, errorField);
        return true;
      }
    }

    // function validateEmailAddress(field, errorField) {
    //   // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
    //   if (!/^[0-9a-zA-Z]{1,3}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
    //     var errMsgEmail = 'The email is not in a valid format. Please use a valid email address.'
    //     showError(field, errorField, errMsgEmail);
    //     return false;
    //   } else {
    //     clearError(field, errorField);
    //     return true;
    //   }
    // }

    // Guest First Name validation
    var guestFirstNameInput = form.querySelector('#id_guest_first_name');
    var guestFirstNameError = document.getElementById('guestFirstNameError');

    // Guest Last Name validation
    var guestLastNameInput = form.querySelector('#id_guest_last_name');
    var guestLastNameError = document.getElementById('guestLastNameError');

    // Guest email address validation
    var guestEmailAddressInput = form.querySelector('#id_guest_email_address');
    var guestEmailAddressError = document.getElementById('guestEmailAddressError');

    // Friend first name validation
    var friendFirstNameInput = form.querySelector('#id_friend_first_name');
    var friendFirstNameError = document.getElementById('friendFirstNameError');

    // Friend email address validation
    var friendEmailAddressInput = form.querySelector('#id_friend_email_address');
    var friendEmailAddressError = document.getElementById('friendEmailAddressError');

    // input event listener
    guestFirstNameInput.addEventListener('input', function () {
      validateName(guestFirstNameInput, guestFirstNameError);
    });
    guestLastNameInput.addEventListener('input', function () {
      validateName(guestLastNameInput, guestLastNameError);
    });
    guestEmailAddressInput.addEventListener('input', function () {
      validateEmailAddress(guestEmailAddressInput, guestEmailAddressError);
    });
    friendFirstNameInput.addEventListener('input', function () {
      validateName(friendFirstNameInput, friendFirstNameError);
    });
    friendEmailAddressInput.addEventListener('input', function () {
      validateEmailAddress(friendEmailAddressInput, friendEmailAddressError);
    });


    // form.addEventListener('submit', function (event) {
    //   alert('All field are valid.');
    // });

  });



// ******************************************************************************
// guestactions-> Contact us form validation
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('myForm');
  // console.log(form, 'line 88')

  // showing error
  function showError(field, errorField, errorMsg){
    errorField.innerHTML = errorMsg;
    field.classList.add('is_invalid'); // add class
  }

  // clearing error
  function clearError(field, errorFiled){
    errorFiled.innerHTML = '';
    field.classList.remove('is_valid'); // remove class
  }

  // use javasctipt regular expression to validation name and email filed
  function validateName(field, errorField) {
    if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
      var errMsgName = 'Special characters are not allowed except letters.'
      showError(field, errorField, errMsgName);
      return false;
    } else {
      clearError(field, errorField);
      return true;
    }
  }

  function validateEmailAddress(field, errorField) {
    // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!/^[0-9a-zA-Z]{1,3}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
      var errMsgEmail = 'The email is not in a valid format. Please use a valid email address.'
      showError(field, errorField, errMsgEmail);
      return false;
    } else {
      clearError(field, errorField);
      return true;
    }
  }

  // take input
  var firstNameInput = document.querySelector('#id_f_name');
  var firstNameError = document.getElementById('firstNameError');

  var lastNameInput = document.querySelector('#id_l_name');
  var lastNameError = document.getElementById('lastNameError');

  var emailInput = document.querySelector('#id_email');
  var emailError = document.getElementById('emailError');

  // user input event listener
  firstNameInput.addEventListener('input', function (){
    validateName(firstNameInput, firstNameError)
  });
  lastNameInput.addEventListener('input', function (){
    validateName(lastNameInput, lastNameError)
  });
  emailInput.addEventListener('input', function (){
    validateEmailAddress(emailInput, emailError)
  });

  // form.addEventListener('submit', () => {
  //   alert('All field are valid. You can submit the data')
  // })
  
});


// **********************************************************************
// guesactions-> Section 2: About you form validation
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('myForm');
  // console.log(form, 'line 88')

  // showing error
  function showError(field, errorField, errorMsg){
    errorField.innerHTML = errorMsg;
    field.classList.add('is_invalid'); // add class
  }

  // clearing error
  function clearError(field, errorFiled){
    errorFiled.innerHTML = '';
    field.classList.remove('is_valid'); // remove class
  }

  // use javasctipt regular expression to validation name and email filed
  function validateName(field, errorField) {
    if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
      var errMsgName = 'Special characters are not allowed except letters.'
      showError(field, errorField, errMsgName);
      return false;
    } else {
      clearError(field, errorField);
      return true;
    }
  }

  function validateEmailAddress(field, errorField) {
    // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!/^[0-9a-zA-Z]{1,}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
      var errMsgEmail = 'The email is not in a valid format. Please use a valid email address.'
      showError(field, errorField, errMsgEmail);
      return false;
    } else {
      clearError(field, errorField);
      return true;
    }
  }

  // take input
  var firstNameInput = document.querySelector('#id_first_name');
  var firstNameError = document.getElementById('firstNameError');

  var lastNameInput = document.querySelector('#id_last_name');
  var lastNameError = document.getElementById('lastNameError');

  var emailInput = document.querySelector('#id_email_address');
  var emailError = document.getElementById('emailError');

  // user input event listener
  firstNameInput.addEventListener('input', function (){
    validateName(firstNameInput, firstNameError);
  });
  lastNameInput.addEventListener('input', function (){
    validateName(lastNameInput, lastNameError);
  });
  emailInput.addEventListener('input', function (){
    validateEmailAddress(emailInput, emailError);
  });

  // form.addEventListener('submit', () => {
  //   alert('All field are valid. You can submit the data')
  // })
  
});


// **********************************************************************
// guesactions->product-review Order status check form validation
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('myForm');
  // console.log(form, 'line 88')

  // showing error
  function showError(field, errorField, errorMsg){
    errorField.innerHTML = errorMsg;
    field.classList.add('is_invalid'); // add class
  }

  // clearing error
  function clearError(field, errorFiled){
    errorFiled.innerHTML = '';
    field.classList.remove('is_valid'); // remove class
  }

  function validateEmailAddress(field, errorField) {
    // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!/^[0-9a-zA-Z]{1,}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
      var errMsgEmail = 'The email is not in a valid format. Please use a valid email address.'
      showError(field, errorField, errMsgEmail);
      return false;
    } else {
      clearError(field, errorField);
      return true;
    }
  }

  // take input
  var emailInput = document.querySelector('#id_email_add');
  var emailError = document.getElementById('emailAddError');

  // user input event listener
  emailInput.addEventListener('input', function (){
    validateEmailAddress(emailInput, emailError)
  });

  // form.addEventListener('submit', () => {
  //   alert('Email is valided. You can submit it now')
  // })
  
});


// **********************************************************************
// guesactions->site-survey  form validation
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('myForm');
  // console.log(form, 'line 276')

  // showing error
  function showError(field, errorField, errorMsg){
    errorField.innerHTML = errorMsg;
    field.classList.add('is_invalid'); // add class
  }

  // clearing error
  function clearError(field, errorFiled){
    errorFiled.innerHTML = '';
    field.classList.remove('is_valid'); // remove class
  }

   // use javasctipt regular expression to validation name and email filed
   function validateName(field, errorField) {
    if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
      var errMsgName = 'Special characters are not allowed except letters.'
      showError(field, errorField, errMsgName);
      return false;
    } else {
      clearError(field, errorField);
      return true;
    }
  }

  function validateEmailAddress(field, errorField) {
    // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!/^[0-9a-zA-Z]{1,}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
      var errMsgEmail = 'The email is not in a valid format. Please use a valid email address.'
      showError(field, errorField, errMsgEmail);
      return false;
    } else {
      clearError(field, errorField);
      return true;
    }
  }

  // take input
  // var fullNameInput = document.querySelector('#id_name');
  // var fullNameError = document.getElementById('fullNameError');

  // var emailInput = document.querySelector('#id_email');
  // var emailError = document.getElementById('emailError');

  // user input event listener
  // fullNameInput.addEventListener('input', function (){
  //   validateName(fullNameInput, fullNameError)
  // });

  // emailInput.addEventListener('input', function (){
  //   validateEmailAddress(emailInput, emailError)
  // });

  // form.addEventListener('submit', () => {
  //   alert('Email is valided. You can submit it now')
  // })
  
});





// // ******************************************************************************
// // guestaction-> invite firends form validation
// document.addEventListener('DOMContentLoaded', function () {
//     alert('reading form insite invite firends...');
//     var form = document.getElementById('myForm');
//     console.log(form, 'line 5')

//     var form1 = document.getElementById("myFormContact")
//     console.log(form1, 'line 9')
//     function showError(field, errorField, errorMessage) {
//       errorField.innerHTML = errorMessage;
//       field.classList.add('is-invalid');
//     }

//     function clearError(field, errorField) {
//       errorField.innerHTML = '';
//       field.classList.remove('is-invalid');
//     }

//     function validateName(field, errorField) {
//       if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
//         var errMsgName = 'Special characters are not allowed except letters.'
//         showError(field, errorField, errMsgName);
//         return false;
//       } else {
//         clearError(field, errorField);
//         return true;
//       }
//     }

//     function validateEmailAddress(field, errorField) {
//       // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
//       if (!/^[0-9a-zA-Z]{1,3}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
//         var errMsgEmail = 'The email is not in a valid format. Please use a valid email address.'
//         showError(field, errorField, errMsgEmail);
//         return false;
//       } else {
//         clearError(field, errorField);
//         return true;
//       }
//     }

//     // Guest First Name validation
//     var guestFirstNameInput = form.querySelector('#id_guest_first_name');
//     var guestFirstNameError = document.getElementById('guestFirstNameError');

//     // Guest Last Name validation
//     var guestLastNameInput = form.querySelector('#id_guest_last_name');
//     var guestLastNameError = document.getElementById('guestLastNameError');

//     // Guest email address validation
//     var guestEmailAddressInput = form.querySelector('#id_guest_email_address');
//     var guestEmailAddressError = document.getElementById('guestEmailAddressError');

//     // Friend first name validation
//     var friendFirstNameInput = form.querySelector('#id_friend_first_name');
//     var friendFirstNameError = document.getElementById('friendFirstNameError');

//     // Friend email address validation
//     var friendEmailAddressInput = form.querySelector('#id_friend_email_address');
//     var friendEmailAddressError = document.getElementById('friendEmailAddressError');

//     // input event listener
//     guestFirstNameInput.addEventListener('input', function () {
//       validateName(guestFirstNameInput, guestFirstNameError);
//     });
//     guestLastNameInput.addEventListener('input', function () {
//       validateName(guestLastNameInput, guestLastNameError);
//     });
//     guestEmailAddressInput.addEventListener('input', function () {
//       validateEmailAddress(guestEmailAddressInput, guestEmailAddressError);
//     });
//     friendFirstNameInput.addEventListener('input', function () {
//       validateName(friendFirstNameInput, friendFirstNameError);
//     });
//     friendEmailAddressInput.addEventListener('input', function () {
//       validateEmailAddress(friendEmailAddressInput, friendEmailAddressError);
//     });

//     // Input-> Guesactions-> Contact us form validation
//     var firstNameInputContact = document.querySelector('#id_f_name');
//     var firstNameErrorContact = document.getElementById('firstNameErrorContact');
  
//     var lastNameInputContact = document.querySelector('#id_l_name');
//     var lastNameErrorContact = document.getElementById('lastNameErrorContact');
  
//     var emailInputContact = document.querySelector('#id_email');
//     var emailErrorContact = document.getElementById('emailErrorContact');

//     // Input EventListener-> Guesactions-> Contact us form validation
//     firstNameInputContact.addEventListener('input', function (){
//       validateName(firstNameInputContact, firstNameErrorContact);
//     });
//     lastNameInputContact.addEventListener('input', function (){
//       validateName(lastNameInputContact, lastNameErrorContact);
//     });
//     emailInputContact.addEventListener('input', function (){
//       validateEmailAddress(emailInputContact, emailErrorContact);
//     });

//     // Input-> Guestactions-> about you form validation
//     var firstNameInput = document.querySelector('#id_first_name');
//     var firstNameError = document.getElementById('firstNameError');
  
//     var lastNameInput = document.querySelector('#id_last_name');
//     var lastNameError = document.getElementById('lastNameError');
  
//     var emailInput = document.querySelector('#id_email_address');
//     var emailError = document.getElementById('emailError');

//     // Input EventListener-> Guestactions-> about you form validation
//     firstNameInput.addEventListener('input', function (){
//       validateName(firstNameInput, firstNameError);
//     });
//     lastNameInput.addEventListener('input', function (){
//       validateName(lastNameInput, lastNameError);
//     });
//     emailInput.addEventListener('input', function (){
//       validateEmailAddress(emailInput, emailError);
//     });

//     // Input-> Guestactions-> Product-review-> Check order status form validation
//     var emailInput = document.querySelector('#id_email_add');
//     var emailError = document.getElementById('emailAddError');

//     // Input EventListener-> Guestactions-> Product-review-> Check order status form validation
//     emailInput.addEventListener('input', function (){
//       validateEmailAddress(emailInput, emailError);
//     });

//     // Input-> Guestactions-> site-servey-> from validation
//     var fullNameInput = document.querySelector('#id_name');
//     var fullNameError = document.getElementById('fullNameError');
  
//     var emailInput = document.querySelector('#id_email');
//     var emailError = document.getElementById('emailError');

//     // Input EventListener-> Guestactions-> site-servey-> from validation
//     fullNameInput.addEventListener('input', function (){
//       validateName(fullNameInput, fullNameError);
//     });

//     emailInput.addEventListener('input', function (){
//       validateEmailAddress(emailInput, emailError);
//     });


//     form.addEventListener('submit', function (event) {
//       alert('All field are valid.');
//     });

// });

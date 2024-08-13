// // ******************************************************************************
// // invite firends form validation
// document.addEventListener('DOMContentLoaded', function () {
//     alert('reading form insite invite firends...');
//     var form = document.getElementById('myForm');

//     function showError(field, errorField, errorMessage) {
//       errorField.innerHTML = errorMessage;
//       field.classList.add('is-invalid');
//     }

//     function clearError(field, errorField) {
//       errorField.innerHTML = '';
//       field.classList.remove('is-invalid');
//     }

//     function validateName(field, errorField) {
//       if (!/^[a-zA-Z]+$/.test(field.value.trim())) {
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


//     form.addEventListener('submit', function (event) {
//       alert('All field are valid.');
//     });
//   });
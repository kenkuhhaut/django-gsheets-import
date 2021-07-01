//
// Copyright (c) 2021, Alexander Helmboldt
//
//
// This file incorporates work covered by the following copyright and  
// permission notice:
//
// Copyright (c) 2020, Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// NOTICE: The code has been modified and extended by Alexander Helmboldt.
//



'use strict';

//
// Template related variables and functions.
//

// relevant input HTML elements for format selection
const select_format = document.getElementById("id_input_format");

// relevant input HTML elements for file selection
const button_import = document.getElementById("id_import_file");
const span_import = document.getElementById("id_import_file_span");
const input_os_file = document.getElementById("id_import_file_os_file");
const input_google_file = document.getElementById("id_import_file_google_id");
const input_google_oauth = document.getElementById("id_import_file_google_oauth_token");
const input_is_google = document.getElementById("id_import_file_is_google");

// additional variables 'developerKey', 'clientId', and 'appId' are
// already set in the 'import.html' template



// add default 'onClick' event for the button
if(button_import) {
    button_import.addEventListener("click", loadFilePicker);
}

// add 'onChange' event for file input tag
if(input_os_file) {
    input_os_file.addEventListener("change", updateOSFileName);
}



// 'onClick' event of the file select button, which distinguishes the 'Google Sheet' format from all other formats
function loadFilePicker(event) {
    const selected_option = select_format.options[select_format.selectedIndex].text
    // load file picker appropriate for Google Sheet format
    if(selected_option === "Google Sheet") {
        input_is_google.value = true
        loadGooglePicker(event)
    // load file picker appropriate for other formats
    } else {
        input_is_google.value = false
        loadOSPicker(event)
    }
}


// trigger the default 'onClick' event of the input tag (type="file")
function loadOSPicker(event) {
    if(input_os_file) {
        input_os_file.click();
    }
}


// write the currently selected OS file to the span element
function updateOSFileName(event) {
    if(span_import) {
        span_import.innerHTML = this.files[0].name
    }
}




//
// Google Picker related variables and functions.
//

// Scope to use to access user's Drive items.
const scope = 'https://www.googleapis.com/auth/drive.file';

// global variables
var pickerApiLoaded = false;
var oauthToken;



// load the google.picker script and gapi.auth2
function loadGooglePicker(event) {
    gapi.load('auth2', {'callback': onAuthApiLoad});
    gapi.load('picker', {'callback': onPickerApiLoad});
}


// Function to call once the 'auth2' library has been successfully loaded. It will perform a one time OAuth 2.0 authorization.
function onAuthApiLoad() {
    window.gapi.auth2.authorize(
        {
            'client_id': clientId,
            'scope': scope,
            'immediate': false
        },
    handleAuthResult);
}


// Function to call once the 'picker' library has been successfully loaded.
function onPickerApiLoad() {
    pickerApiLoaded = true;
    createPicker();
}


// Function to call once the authorization request has been completed (either successfully or with a failure).
// The 'authResult' argument is an object of class 'gapi.auth2.AuthorizeResponse'.
function handleAuthResult(authResult) {
    if (authResult && !authResult.error) {
        oauthToken = authResult.access_token;
        createPicker();
    }
}


// Create and render a Picker object.
function createPicker() {
    if (pickerApiLoaded && oauthToken) {
        var view = new google.picker.View(google.picker.ViewId.SPREADSHEETS);
        var picker = new google.picker.PickerBuilder()
            .enableFeature(google.picker.Feature.NAV_HIDDEN)
            .setAppId(appId)
            .setOAuthToken(oauthToken)
            .addView(view)
            .setDeveloperKey(developerKey)
            .setCallback(pickerCallback)
            .build();
        picker.setVisible(true);
    }
}


// Function to call once the picker was successfully built.
function pickerCallback(data) {
    if (data.action == google.picker.Action.PICKED) {
        input_google_file.value = data.docs[0].id;
        input_google_oauth.value = oauthToken;
        span_import.innerHTML = data.docs[0].name + " (1st sheet)";
    }
}

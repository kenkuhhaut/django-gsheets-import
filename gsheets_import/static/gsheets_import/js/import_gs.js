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

// relevant HTML elements for file selection
const button_import = document.getElementById("id_import_file");
const span_import = document.getElementById("id_import_file_span");
const input_os_file = document.getElementById("id_import_file_os_file");
const input_google_file = document.getElementById("id_import_file_google_id");
const input_google_oauth = document.getElementById("id_import_file_google_oauth_token");
const input_is_google = document.getElementById("id_import_file_is_google");




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

// Discovery document for the Google Sheets API
const discoveryDoc = ['https://sheets.googleapis.com/$discovery/rest?version=v4'];

// global variables
var pickerApiLoaded = false;
var oauthToken;
var googleAuth;

// additional variables 'developerKey', 'clientId', and 'appId' are
// already set in the 'import.html' template



// Load the necessary libraries (executed once "https://apis.google.com/js/api.js" has finished loading)
function loadLibraries() {
    console.log("+++ loadLibraries");
    gapi.load('client:auth2', {'callback': onClientLoad});
    gapi.load('picker', {'callback': () => { pickerApiLoaded = true; }});
}


// Initialize the client library (executed once the client and the auth2 libraries have finished loading)
function onClientLoad() {
    gapi.client.init({
        'apiKey': developerKey,
        'discoveryDocs': discoveryDoc,
        'clientId': clientId,
        'scope': scope,
        'immediate': false
    }).then(function() {
        // initialize global GoogleAuth object and assign listener function
        googleAuth = gapi.auth2.getAuthInstance();
        googleAuth.isSignedIn.listen(updateSignInStatus);
    }).then(function() {
        // add 'onChange' event for file input tag
        if(input_os_file) {
            input_os_file.addEventListener("change", updateOSFileName);
        }
        // add default 'onClick' event for the button and remove disabled property
        if(button_import) {
            button_import.addEventListener("click", loadFilePicker);
            button_import.disabled = false;
        }
    }).catch(function(error) {
        // error handling
        console.log("+++ This somehow failed");
        console.log(error);
    })
}


// Function that is called once the sign-in status changes
// (argument: true if user is signing in, false if signing out)
function updateSignInStatus(isSignedIn) {
    console.log("+++ updateSignInStatus 1" + isSignedIn)
    if(isSignedIn) {
        console.log("+++ updateSignInStatus 2")
        oauthToken = googleAuth.currentUser.get().getAuthResponse().access_token;
        createPicker();
    }
}


// Start the OAuth 2.0 authentication flow if the user is not signed in yet
function loadGooglePicker(event) {
    var isSignedIn = googleAuth.isSignedIn.get();
    console.log("+++ loadGooglePicker 1" + isSignedIn)
    if(isSignedIn) {
        oauthToken = googleAuth.currentUser.get().getAuthResponse().access_token;
    } else {
        googleAuth.signIn();
    }
    createPicker();
    console.log("+++ loadGooglePicker 2")
}


// Create and render a Picker object.
function createPicker() {
    console.log("+++ pickerApiLoaded: " + pickerApiLoaded + " oauthToken: " + oauthToken);
    if(pickerApiLoaded && oauthToken) {
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
    if(data.action == google.picker.Action.PICKED) {
        input_google_file.value = data.docs[0].id;
        input_google_oauth.value = oauthToken;
        span_import.innerHTML = data.docs[0].name + " (1st sheet)";

        /* display all subsheets
        gapi.client.sheets.spreadsheets.get({
            spreadsheetId: data.docs[0].id
        }).then(function(response) {
            console.log(response.result.sheets)
        }).catch(function(response) {
            console.log('Error: ' + response.result.error.message);
        });
        */
    }
}


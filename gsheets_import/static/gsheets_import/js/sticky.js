'use strict';


// import helper functions
import { getAbsOffsetTop, getScrollbarHeight } from './sticky_helpers.js'



// div containing the preview table (no error case)
const container_div = document.getElementById('no-error-container');

// Django content and footer divs
const content_div = document.getElementById('content');
const footer_div = document.getElementById('footer');

// preview table (no error case)
const no_error_table = document.getElementById('no-error-table');



// Function to dynamically set the height of the container div.
//      * If the table (+ horizontal scrollbar height) fully fits on the screen, set the height automatically.
//      * If not, set the height such that the div fills the remaining screen.
function resizeDivHeight(event) {
    if(container_div) {
        let view_height = 0, table_height = 0, available_height = 0;
        const body = window.document.body;

        if(window.innerHeight) {
            view_height = window.innerHeight;
        } else if(body.parentElement.clientHeight) {
            view_height = body.parentElement.clientHeight;
        } else if(body && body.clientHeight) {
            view_height = body.clientHeight;
        }

        // height of the table + a horizontal scrollbar
        table_height = no_error_table.offsetHeight + getScrollbarHeight();
        // remaining height that is available without having to add vertical scrollbars to body
        available_height = view_height - getAbsOffsetTop(container_div)
                - parseFloat(window.getComputedStyle(content_div).paddingBottom)
                - footer_div.offsetHeight;

        // decide how to set the height of the container div ...
        // ... fixed height so that a vertical scrollbar for the container div appears and sticky headers are possible at the same time
        if(table_height > available_height) {
            container_div.style.height = (available_height + "px");
        // ... automatic height so that the paginator is always right beneath the table (regardless of whether a horizontal scrollbar is present or not)
        } else {
            container_div.style.height = "auto";
        }
    }
}



// reset the container div height on load and on resize
window.addEventListener('load', resizeDivHeight);
window.addEventListener('resize', resizeDivHeight);

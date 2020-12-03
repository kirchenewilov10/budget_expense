// *************** Get Cookie *************** //
function get_cookie(name) {
	var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// *************** Get CSRF Token *************** //
function get_csrf_token() {
	return get_cookie("csrftoken");
}

// *************** Show Loading Gif *************** //
function show_loading() {
    $("#loading").css("display", "block");
    $("#waiting").addClass("modal-backdrop fade in");
}

// *************** Hide Loading Gif *************** //
function hide_loading() {
    $("#loading").css("display", "none");
    $("#waiting").removeClass("modal-backdrop fade in");
}

// *************** Show Info Toastr *************** //
function show_info_toastr(title, message) {
    toastr.info(message, title);
}

// *************** Show Success Toastr *************** //
function show_success_toastr(title, message) {
    toastr.success(message, title);
}

// *************** Show Warning Toastr *************** //
function show_warning_toastr(title, message) {
    toastr.warning(message, title);
}

// *************** Show Error Toastr *************** //
function show_error_toastr(title, message) {
    toastr.error(message, title);
}

// *************** Fix String *************** //
function fix_string(str) {
    return str.replace(/slashn/g, "\n").replace(/&#39;/g, "'").replace(/slashopposite/g, "\\");
}

// *************** Date To String (1) *************** //
function date_to_str_1(date_obj) {
    var year = date_obj.getFullYear();
    var month = date_obj.getMonth() + 1;
    var day = date_obj.getDate();
    if (month < 10)
        month = "0" + month;
    if (day < 10)
        day = "0" + day;
    return [year, month, day].join("-");
}

// *************** Generate Random String *************** //
function random_string(string_length) {
    /*Charecters you want to use for your Random String*/
    var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
    var randomstring = '';

    for (var i = 0; i < string_length; i++) {
    var rnum = Math.floor(Math.random() * chars.length);
    randomstring += chars.substring(rnum, rnum + 1);
    }
    return randomstring;
}

// *************** Draw Column Chart *************** //
function draw_column_chart(id, data, x_axis_key, y_axis_key, title, tooltip_format, x_axis_type) {
    var chart = am4core.create(id, am4charts.XYChart);
    chart.data = data;

    let title_text = chart.titles.create();
    title_text.text = title;
    title_text.fontSize = 25;
    title_text.marginBottom = "10px";
    title_text.fill = am4core.color("#000");

    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = x_axis_key;
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.minGridDistance = 30;
    categoryAxis.renderer.labels.template.rotation = 10;
    categoryAxis.renderer.labels.template.fill = am4core.color("#000");
    categoryAxis.renderer.grid.template.stroke = am4core.color("#000");
    categoryAxis.renderer.grid.template.strokeOpacity = 0.3;

    categoryAxis.renderer.labels.template.adapter.add("dy", function(dy, target) {
        if (x_axis_type == 2 && target.dataItem && target.dataItem.index & 2 == 2) {
            return dy + 25;
        }
        return dy;
    });

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.renderer.labels.template.fill = am4core.color("#000");
    valueAxis.renderer.grid.template.stroke = am4core.color("#000");
    valueAxis.renderer.grid.template.strokeOpacity = 0.3;

    // Create series
    var series = chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = y_axis_key;
    series.dataFields.categoryX = x_axis_key;
    series.name = "Project";
    series.columns.template.tooltipText = tooltip_format;
    series.columns.template.fillOpacity = .8;

    var columnTemplate = series.columns.template;
    columnTemplate.strokeWidth = 2;
    columnTemplate.strokeOpacity = 1;
}


var alert_str = new Array();
// --------------- 0x1xxxxx For Admin Panel --------------- //
alert_str["0x10001"] = {
    "title": "",
    "message": "Please enter all information."
};

alert_str["0x10002"] = {
    "title": "",
    "message": "User has been registered."
};

alert_str["0x10003"] = {
    "title": "",
    "message": "User has been updated."
};

alert_str["0x10004"] = {
    "title": "",
    "message": "User has been deleted."
};

alert_str["0x10005"] = {
    "title": "",
    "message": "Max count of answer is 10."
};

alert_str["0x10006"] = {
    "title": "",
    "message": "Min count of answer is 2."
};

alert_str["0x10007"] = {
    "title": "",
    "message": "Invalid question"
};

alert_str["0x10008"] = {
    "title": "",
    "message": "There is one or more answers with no text."
};

alert_str["0x10009"] = {
    "title": "",
    "message": "Test has an invalid title."
};

alert_str["0x1000A"] = {
    "title": "",
    "message": "Test has to have at least two quizes."
};

alert_str["0x1000B"] = {
    "title": "",
    "message": "Test is saved."
};

alert_str["0x1000C"] = {
    "title": "",
    "message": "Invalid category name"
};

alert_str["0x1000D"] = {
    "title": "",
    "message": "There is one or more answers with no category."
};

alert_str["0x1000E"] = {
    "title": "",
    "message": "One or more quizes are already using this category."
};

alert_str["0x1000F"] = {
    "title": "",
    "message": "Test has been assigned."
};

alert_str["0x10010"] = {
    "title": "",
    "message": "Test is already completed."
};

alert_str["0x10011"] = {
    "title": "",
    "message": "Test has been deleted."
};

alert_str["0x10012"] = {
    "title": "",
    "message": "Invalid max rating"
};

alert_str["0x10013"] = {
    "title": "",
    "message": "Invalid category"
};

alert_str["0x10014"] = {
    "title": "",
    "message": "Please enter user email."
};

alert_str["0x10015"] = {
    "title": "",
    "message": "There is no registered user with this email."
};

alert_str["0x10016"] = {
    "title": "",
    "message": "Status of test has been updated."
};

alert_str["0x10017"] = {
    "title": "",
    "message": "You can't update status of test that is already completed."
};

alert_str["0x10018"] = {
    "title": "",
    "message": "Test is completed."
};

alert_str["0x10019"] = {
    "title": "",
    "message": "Please select test"
};

alert_str["0x1001A"] = {
    "title": "",
    "message": "Test is not available to edit because it's already assigned."
};

alert_str["0x1001B"] = {
    "title": "",
    "message": "Test is duplicated."
};

alert_str["0x1001C"] = {
    "title": "",
    "message": "File size should be under 2Mbyte."
};

alert_str["0x1001D"] = {
    "title": "",
    "message": "Sorry, error occured while importing test from file."
};

alert_str["0x1001E"] = {
    "title": "",
    "message": "Invalid test format"
};

alert_str["0x1001F"] = {
    "title": "",
    "message": "Test is imported."
};

alert_str["0x10020"] = {
    "title": "",
    "message": "Profile is updated."
};


// --------------- 0x2xxxxx For User Panel --------------- //
alert_str["0x20001"] = {
    "title": "",
    "message": "Please select an answer."
};

alert_str["0x20002"] = {
    "title": "",
    "message": "Sorry, error occured while generating report."
};

// --------------- 0xFxxxxx For Others --------------- //
alert_str["0xF0001"] = {
    "title": "",
    "message": "Sorry, something went wrong."
};



$(document).ajaxError(function(event, xhr, ajaxOptions, thrownError) {

});
$( document ).ajaxComplete(function( event, xhr, settings ) {

});
$( document ).ajaxSend(function( event, xhr, settings ) {
    xhr.setRequestHeader("X-CSRFToken", get_csrf_token());
});

function ajax_common_result_handler(ret_code){
    if (ret_code === "success"){
        show_success_toastr("", "Operation success.");
    } else if (ret_code === "failure"){
        show_error_toastr("", "Sorry, Operation failure.");
    }
}
function reload_page(){
    setTimeout(function() {
        window.location.reload();
    }, 1000);
}

function valid_email_pattern(string){
    if (string.trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) === null) {
        return false;
    }
    return true;
}

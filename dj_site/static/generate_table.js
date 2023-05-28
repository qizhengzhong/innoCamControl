


var currentRow = 0

function addRow() {

    const form = document.getElementById("formContainer");
    const row = document.createElement("div");
    const dropDownElement = document.createElement("div");

    var dropDownID = "dropdown" + currentRow.toString();
    var label = document.createElement("div");

    label.classList.add("form-label");
    label.setAttribute("for", dropDownID);
    label.innerHTML = "Select Building Block";

    var input = document.createElement("select");
    input.classList.add("form-select");
    input.id = dropDownID;

    var option = document.createElement("option");
    option.setAttribute("selected","");
    option.innerHTML = "Default Option";

    input.appendChild(option);
    dropDownElement.appendChild(label);
    dropDownElement.appendChild(input);

    const jsonElement = document.createElement("div");
    var jsonID = "json" + currentRow.toString();

    var label = document.createElement("div");
    label.classList.add("form-label");
    label.setAttribute("for", jsonID)
    label.innerHTML = "Select Options"

    var input = document.createElement("input");
    input.classList.add("form-control");
    input.setAttribute("type", "text");
    input.id = jsonID;

    jsonElement.appendChild(label);
    jsonElement.appendChild(input);


    row.classList.add("row", "mb-3");
    dropDownElement.classList.add("col-4");
    jsonElement.classList.add("col-8");


    form.insertBefore(row, document.getElementById("button_row"))
    row.appendChild(dropDownElement);
    row.appendChild(jsonElement);



    currentRow += 1;
}

function addRow2() {
    const node = document.getElementById("default_form_row");
    const clone = node.cloneNode(true);

    clone.classList.remove("d-none");
    clone.id = "form_row" + currentRow.toString();
    


    clone.querySelector("#dropdown").setAttribute("name", "dropdown_" + currentRow.toString());
    clone.querySelector("#json").setAttribute("name", "json_" + currentRow.toString());
    clone.querySelector("#dropdown_label").setAttribute("name", "dropdown_" + currentRow.toString());
    clone.querySelector("#json_label").setAttribute("name", "json_" + currentRow.toString());


    const form = document.getElementById("form_container");
    form.insertBefore(clone, document.getElementById("button_row"));

    currentRow += 1;
}

document.onload = addRow2();
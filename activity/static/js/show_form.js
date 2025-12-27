$(document).ready(function () {
    const acitivityForm = $("#add-activity-form");
    const addButton = $("#add-activity-button");

    acitivityForm.hide();

    addButton.click(function () {
        if (acitivityForm.is(":visible")) {
            acitivityForm.hide();
            addButton.text("Add");
        } else {
            addButton.text("Hide");
            acitivityForm.toggle();
        }
    });
});

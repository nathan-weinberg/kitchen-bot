function populateSelect() {

	var select = document.getElementById("dynamic-select");
	select.options[select.options.length] = new Option ("None", "NONE");

	$.post("/", function(boysJSON) {
		for (index in boysJSON) {
			select.options[select.options.length] = new Option (boysJSON[index], index)
		}
	});

}
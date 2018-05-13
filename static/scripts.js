function populateSelect() {

	var select = document.getElementById("dynamic-select");
	select.options[select.options.length] = new Option ("None", "NONE");
	select.options[select.options.length] = new Option ("All", "ALL");

	$.post("/", function(boysJSON) {
		for (index in boysJSON) {
			select.options[select.options.length] = new Option (boysJSON[index], index)
		}
	});

}
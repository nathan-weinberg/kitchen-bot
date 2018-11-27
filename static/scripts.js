function populateSelect() {

	var select = document.getElementById("dynamic-select");
	select.options[select.options.length] = new Option ("None", "NONE");
	select.options[select.options.length] = new Option ("All", "ALL");

	$.post("/select", function(boysJSON) {
		for (index in boysJSON) {
			select.options[select.options.length] = new Option (boysJSON[index], index)
		}
	});

}

function viewSchedule() {

	$.post("/schedule", function(data) {

		var table = document.createElement("TABLE");
		table.setAttribute("id", "scheduleTable");
		document.getElementById("table").appendChild(table);

		var legend = document.createElement("TR");
		legend.setAttribute("id", "rowLegend");
		document.getElementById("scheduleTable").appendChild(legend)

		var name = document.createElement("TD");
		var t1 = document.createTextNode("name");
		name.appendChild(t1);
		document.getElementById("rowLegend").appendChild(name);

		var isboy = document.createElement("TD");
		var t2 = document.createTextNode("isboy");
		isboy.appendChild(t2);
		document.getElementById("rowLegend").appendChild(isboy);

		var nextboy = document.createElement("TD");
		var t3 = document.createTextNode("nextboy");
		nextboy.appendChild(t3);
		document.getElementById("rowLegend").appendChild(nextboy);

		var daynum = document.createElement("TD");
		var t4 = document.createTextNode("daynum");
		daynum.appendChild(t4);
		document.getElementById("rowLegend").appendChild(daynum);

		for (index in data) {
			var temp = document.createElement("TR");
			temp.setAttribute("id", "row" + String(index));
			document.getElementById("scheduleTable").appendChild(temp);
			for (subindex in data[index]) {
				var temp2 = document.createElement("TD");
				var temp3 = document.createTextNode(data[index][subindex]);
				temp2.appendChild(temp3);
				document.getElementById("row" + String(index)).appendChild(temp2);
			}
		}

	});

}

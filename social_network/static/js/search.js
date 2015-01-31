
function populateSearchTable(whichPage) {
    
    if (whichPage == undefined)
	whichPage = 0;

    //Create header
    header = "<h1>Welcome to the Volunteer Job Search Page!</h1>";


    

    tableContents = ""
    $.ajax({
	type: "GET",
	url: "/social/search_backend/",
	data: {
	    search_vals : "all",
	    per_page: 10,
	    page : whichPage
	}
    })
	.done(function( msg ) {
	    var jsonObj = JSON.parse(msg);

	    var numPages;
	    
	    if (jsonObj.length>0) {
		numPages = jsonObj[0].numPages;
	    }
	    else {
		$("#job_search_div").html("<h3>Error: No jobs found!</h3>");
		return;
	    }

	    
	    header += "<div class='page_select' id='page_select_div'>";

	    for (i = 1; i<=Math.min(numPages, 9); i++) {
		if ((i-1)==whichPage)
		    header += i;
		else
		    header += "<a href='#' class='page_num_link' onclick='populateSearchTable("+(i-1)+");' >" + i + "</a>";
	    }

	    if (numPages>9) {
		if ((numPages-1)==whichPage)
		    header += "..."+numPages;
		else
		    header+="...<a href='#' class='page_num_link' onclick='populateSearchTable("+(numPages-1)+");' >" + numPages + "</a>";

	    }
	    
	    header += "</div>";
	    
	    tableContents+="<div class='job_entry_div'>";
	    for (i = 0; i<jsonObj.length ; i++) {
		var curObj = jsonObj[i];
		tableContents+="<div class='job_entry'>";
		tableContents+="<h1 class='job_entry_title'>"+curObj.title+"</h1>";

		tableContents+="<h3 class='job_entry_subtitle'>"+curObj.posted_timestamp+"</h3>";
		tableContents+="<h3 class='job_entry_subtitle'>"+curObj.deadline_date+"</h3>";
		tableContents+="<h3 class='job_entry_subtitle'>"+curObj.job_duration+"</h3>";
		
		tableContents+="<p class='job_entry_descr'>"+curObj.job_descr+"</p>";		
		tableContents+="</div>";

	    }
	    tableContents+="</div>";

	    $("#job_search_div").html(header+tableContents);

	});
    

    

}

$(document).ready(function () {
    populateSearchTable();
});

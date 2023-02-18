function updateData() {
    var sortBy = document.getElementById("sort_by").value;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/view_commission/?sort_by=" + sortBy);
    xhr.send();
  }
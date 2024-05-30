const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

var columnIndex = {
  'num': 0,
  'db_text': 1,
  'file_text': 2,
  'match_percentage': 3
};

var sortDirection = {
  'num': 1,
  'db_text': 1,
  'file_text': 1,
  'match_percentage': 1
};

function sortColumn(columnName) {
  var table, rows, i;
  table = document.getElementById("example");
  rows = table.rows;

  // Toggle sort direction
  sortDirection[columnName] *= -1;

  // Sort the table
  var sortedRows = Array.from(rows).slice(1); // Exclude header row
  sortedRows.sort(function(a, b) {
      var x = extractValue(a.cells[columnIndex[columnName]].innerText.trim(), columnName);
      var y = extractValue(b.cells[columnIndex[columnName]].innerText.trim(), columnName);
      return sortDirection[columnName] * (x - y);
  });

  // Reorder the table rows
  for (i = 0; i < sortedRows.length; i++) {
      table.appendChild(sortedRows[i]);
  }
}

function extractValue(str, columnName) {
  if (columnName === 'match_percentage') {
      // Extract numeric value from the percentage string
      return parseFloat(str.replace('%', ''));
  } else {
      return columnName === 'num' ? parseInt(str) : str;
  }
}

////////////////////////////////////////

var columnIndex1 = {
  'num1': 0,
  'db_text1': 1,
  'file_text1': 2,
  'match_percentage1': 3
};

var sortDirection1 = {
  'num1': 1,
  'db_text1': 1,
  'file_text1': 1,
  'match_percentage1': 1
};

function sortColumn1(columnName1) {
  var table1, rows1, i;
  table1 = document.getElementById("example1");
  rows1 = table1.rows;

  // Toggle sort direction
  sortDirection1[columnName1] *= -1;

  // Sort the table
  var sortedRows1 = Array.from(rows1).slice(1); // Exclude header row
  sortedRows1.sort(function(a, b) {
      var x1 = extractValue(a.cells[columnIndex1[columnName1]].innerText.trim(), columnName1);
      var y1 = extractValue(b.cells[columnIndex1[columnName1]].innerText.trim(), columnName1);
      return sortDirection1[columnName1] * (x1 - y1);
  });

  // Reorder the table rows
  for (i = 0; i < sortedRows1.length; i++) {
      table1.appendChild(sortedRows1[i]);
  }
}

function extractValue(str1, columnName1) {
  if (columnName1 === 'match_percentage1') {
      // Extract numeric value from the percentage string
      return parseFloat(str1.replace('%', ''));
  } else {
      return columnName1 === 'num1' ? parseInt(str1) : str1;
  }
}















const pdf_btn = document.querySelector('#toPDF');

const table = document.querySelector('#t3');
const per = document.querySelector('#t2');
const head=document.querySelector('#t1')
const toPDF = function (table,head,per) {

  // Fetch the CSS file content
  fetch('static/css/style.css')
    .then(response => response.text())
    .then(css => {
      const html_code = `
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style media="all">${css}</style> <!-- Inject CSS styles -->

      </head>
      <body>

          <h1 style="text-align: center;" id="t1"><label class="ddff" id="t2">${per.innerHTML}</label>${head.innerHTML}</h1>
          <div class="m-5" id="t3">${table.innerHTML}</div>
      </body>
     `;
     const new_window = window.open();
      new_window.document.write(html_code);

      setTimeout(() => {
          new_window.print();
          new_window.close();
      }, 400);
    });
}

pdf_btn.onclick = () => {
  toPDF(table,head,per);
}


function toggleTable() {
  document.getElementById("example").classList.toggle("hidden");
  document.getElementById("btnDeleteChecked").classList.toggle("hidden");
  if (document.querySelector('#btnName').value === 'استعراض قاعدة البيانات')
    document.querySelector('#btnName').value = 'اخفاء';
 else
    document.querySelector('#btnName').value = 'استعراض قاعدة البيانات';
}

 document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('btnDeleteChecked').addEventListener('click', function() {
    var form = document.getElementById('deleteForm');
    var checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
    if (checkboxes.length > 0) {
        form.submit();
      } else {
          alert('Please select at least one row to delete.');
        }
    });
});




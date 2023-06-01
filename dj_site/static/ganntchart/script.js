function findStringBetweenFirstAndFinalPipe(str) {
  const firstIndex = str.indexOf('|');
  const lastIndex = str.lastIndexOf('|');
  
  if (firstIndex !== -1 && lastIndex !== -1 && firstIndex !== lastIndex) {
    return str.substring(firstIndex + 1, lastIndex);
  } else {
    return '';
  }
}

function convertStringToTableArray(str) {
  const rows = str.split('||');
  const tableArray = rows.map(row => row.split('|').map(cell => cell.trim()));
  return tableArray;
}
Date.prototype.addDays = function(days) {
  var date = new Date(this.valueOf());
  date.setDate(date.getDate() + days);
  return date;
}


// const userInput = prompt('Enter a string containing "|" symbols:');
const userInput = "Task Name|Task Priority|Task Dependencies|Number of People Needed|Expected Duration||Obtain necessary permits and approvals|High|None|1|1|day||Demolish existing obstacles|Medium|Obtain necessary permits and approvals|2|1 day||Construct partition walls|High|Demolish existing obstacles|3|3 days||Install wooden door frame|Medium|Construct partition walls|2|1 day||Apply first layer of stucco|Medium|Install wooden door frame|2|1 day||Apply second layer of stucco|Medium|Apply first layer of stucco|2|1 day||Prepare surfaces for painting|Medium|Apply second layer of stucco|2|1 day||Apply first layer of white latex paint|Medium|Prepare surfaces for painting|2|1 day||Apply second layer of white latex paint|Medium|Apply first layer of white latex paint|2|1 day||Perform touch-ups on painted walls|Low|Apply second layer of white latex paint|1|1 day|";
const stringtable = findStringBetweenFirstAndFinalPipe(userInput);
const result = convertStringToTableArray(stringtable)

let tasks = [];
for (let i = 1; i < result.length; i++) {
  const row = result[i];
  let task = {
    id: row[0],
    name: row[0],
    start: new Date().toJSON().slice(0,10).replace(/-/g,'-'),
    end: new Date().addDays(Number(row[4].split(' ')[0])).toJSON().slice(0,10).replace(/-/g,'-'),
    progress: 0,
    dependencies: row[2],
  }
  tasks.push(task)
}

let ganttChart = new Gantt("#gantt", tasks, {custom_popup_html: function(task) {
return `
  <div class="details-container">
    <h5>${task.name}</h5>
    <p>Task started on: ${task._start.getDate()}</p>
    <p>Expected to finish by ${task._end.getDate()}</p>
    <p>${task.progress}% completed!</p>
  </div>
`;
}
});

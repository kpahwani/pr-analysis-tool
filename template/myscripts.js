function submitFunction() {
let usernameEle = document.getElementById('username');
let repoEle = document.getElementById('repo');
let column2 = document.querySelector(".column2")
    let username = usernameEle.value;
    let repo = repoEle.value;
    console.log("submitFunction", username, repo, username.length, repo.length)
    if (!username.length || !repo.length) return false;

    let url = "http://127.0.0.1:5000/comments"
    return fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            "repo": repo,
            "author": username
        }),
        headers:{
            Accept: 'application/json',
        },
    })
    .then(function(response) {
        return response.json();})
    .then((response) => {
        let data = response.data
        console.log("res", data);
        column2.style.display = "block";
        var chart = new CanvasJS.Chart("chartContainer", {
            animationEnabled: true,
            theme: "light1", // "light1", "light2", "dark1", "dark2"
            title:{
                text: "PR Comments Report"
            },
            axisY: {
                title: "Comments Count"
            },
            data: [{        
                type: "column",  
                showInLegend: true, 
                legendMarkerColor: "grey",
                legendText: "Comments Type",
                dataPoints: [      
                    { y: data["No review comments"], label: "No review comments" },
                    { y: data["Minor"],  label: "Minor" },
                    { y: data["Moderate"],  label: "Moderate" },
                    { y: data["Critical"],  label: "Critical" },
                ]
            }]
        });
        chart.render();
    })
    .catch(() => {
        column2.style.display = "none";
    })
    .finally(() => {
        console.log("finally")
        return false;
    })
}

function usernameFocus() {
    usernameEle.value = '';
    repoEle.value = '';
    column2.style.display = "none";
    return false;
}
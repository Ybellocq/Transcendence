document.addEventListener("DOMContentLoaded", function() {
    var colors = ['#007bff','#333333'];
    var chartsOptions = {
        cutoutPercentage: 85, 
        legend: {position:'bottom', padding:5, labels: {pointStyle:'circle', usePointStyle:true}}
    };
    var chDonutData = {
        labels: ['Victoires', 'Défaites'],
        datasets: [
            {
                backgroundColor: colors.slice(0, 1),
                borderWidth: 0,
                data: [110, 0]
            }
        ]
    };
    var chDonut = document.getElementById("myChart");
    if (chDonut) {
        new Chart(chDonut, {
            type: 'pie',
            data: chDonutData,
            options: chartsOptions
        });
    }
});
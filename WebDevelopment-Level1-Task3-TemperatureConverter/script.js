document.getElementById('tempInput').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        convert();
    }
});

function convert() {

    var inputBox = document.getElementById('tempInput');
    var unitBox = document.getElementById('unitSelect');
    var errorMsg = document.getElementById('errorMsg');
    var alertBox = document.getElementById('alertBox');
    var results = document.getElementById('results');

    errorMsg.textContent = '';
    alertBox.style.display = 'none';
    results.innerHTML = '<p class="placeholder-text">↑ Enter a value above and press Convert</p>';

    var rawInput = inputBox.value.trim();

    if (rawInput === '') {
        errorMsg.textContent = 'Please enter a temperature value.';
        return;
    }


    var value = parseFloat(rawInput);

    if (isNaN(value)) {
        errorMsg.textContent = "That doesn't look like a number. Try something like 100 or -40.";
        return;
    }

    var celsius;
    var selectedUnit = unitBox.value;

    if (selectedUnit === 'C') {
        celsius = value;

    } else if (selectedUnit === 'F') {
        celsius = (value - 32) * (5 / 9);

    } else {
        celsius = value - 273.15;
    }

    if (celsius < -273.15) {
        alertBox.style.display = 'block';
        return;
    }

    var fahrenheit = (celsius * (9 / 5)) + 32;
    var kelvin = celsius + 273.15;

    var conversions = [
        { label: 'Celsius', value: celsius, unit: '°C' },
        { label: 'Fahrenheit', value: fahrenheit, unit: '°F' },
        { label: 'Kelvin', value: kelvin, unit: 'K' }
    ];

    results.innerHTML = '';

    conversions.forEach(function (item) {

        var card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML =
            '<span class="result-label">' + item.label + '</span>' +
            '<span>' +
            '<span class="result-value">' + item.value.toFixed(2) + '</span>' +
            '<span class="result-unit">' + item.unit + '</span>' +
            '</span>';

        results.appendChild(card);
    });

} 

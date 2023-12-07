document.addEventListener('DOMContentLoaded', getMaxBluCoin);

function getMaxBluCoin() {
  fetch('http://wafer.revs.ir/api/balance?username=aliu')
    .then(response => response.json())
    .then(data => {
      const balanceElement = document.getElementById('max-blu');
      balanceElement.textContent = `Max. ${data.blu} BluCoins`;
      var inputElement = document.getElementById('input-quantity');
      inputElement.setAttribute('max', data.blu);
    })
    .catch(error => {
      console.error('Error:', error);
      const balanceElement = document.getElementById('balance');
      balanceElement.textContent = 'Error occurred while fetching balance.';
    });
}

document.addEventListener('DOMContentLoaded', putCoins);
var selectElement = document.getElementById('all-cryptos');
function putCoins() {
    fetch('http://wafer.revs.ir/api/all_cryptos')
    .then(response => response.json())
    .then(coinsData => {
      coinsData.forEach(coin => {
        var option1 = document.createElement('option');
        option1.value = coin.symbol;
        option1.textContent = coin.name;
        selectElement.appendChild(option1);
      });
    })
    .catch(error => {
      console.error('Error fetching coins list:', error);
    });
}
function updateBuyingCryptoAmout() {
    var selectElement = document.getElementById('all-cryptos');
    var selectedOption = selectElement.options[selectElement.selectedIndex].value;

    var numberInput = document.getElementById('input-quantity');
    var resultElement = document.getElementById('output-quantity');

    var number = numberInput.value;

    document.getElementById('transfer-amount').innerHTML = number + ' ' + "Blu";


    // Send the request to the server
    fetch('http://wafer.revs.ir/api/convert?from_crypto_symbol=blu&to_crypto_symbol=' + selectedOption + '&amount=' + number)
      .then(response => response.json())
      .then(data => {
        // Update the HTML variable with the response
        resultElement.placeholder = data.converted_amount;
      })
      .catch(error => {
        console.log('Error:', error);
      });
  }

function buyC() {
    var numberInput = document.getElementById('input-quantity');
    var number = numberInput.value;

    var selectElement = document.getElementById('all-cryptos');
    var selectedOption = selectElement.options[selectElement.selectedIndex].value;

      fetch('http://wafer.revs.ir/api/transaction/create/?username=aliu&crypto_symbol='+ selectedOption +'&transaction_type=buy&amount='+ number, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
      })
      .then(response => {
        if (response.ok) {
          console.log('Buy request sent successfully');
        } else {
          console.log('Error:', response.status);
        }
      })
      .catch(error => {
        console.log('Error:', error);
      });
}
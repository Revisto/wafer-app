document.addEventListener('DOMContentLoaded', getCryptoWallet);
const walletListElement = document.getElementById('favorites');
function getCryptoWallet() {
  fetch('http://wafer.revs.ir/api/balance?username=aliu')
    .then(response => response.json())
    .then(coinsData => {
      const coinListElement = document.getElementById('favorites');

      const coinSymbols = Object.keys(coinsData);

      coinSymbols.forEach(coinSymbol => {
        fetch(`http://wafer.revs.ir/api/current?crypto_symbol=${coinSymbol}`)
          .then(response => response.json())
          .then(coinData => {
            const listItem = document.createElement('li');
            listItem.setAttribute('class', 'mt-16');
            listItem.innerHTML = `
              <a href="wallet.html" class="coin-item style-2 gap-12">
                <img src="images/coin/${coinSymbol}.jpg" alt="img" class="img" style="border-radius: 50%;">
                <div class="content">
                  <div class="title">
                    <p class="mb-4 text-button">${coinSymbol}</p>
                    <span class="text-secondary">$${coinData.USD}</span>
                  </div>
                  <div class="d-flex align-items-center gap-12">
                    <span class="text-small">$${coinsData[coinSymbol]}</span>
                  </div>
                </div>
              </a>
            `;
            walletListElement.appendChild(listItem);
          })
          .catch(error => {
            console.error(`Error fetching ${coinSymbol} price:`, error);
            const listItem = document.createElement('li');
            listItem.textContent = `Error occurred while fetching ${coinSymbol} price.`;
            walletListElement.appendChild(listItem);
          });
      });
    })
    .catch(error => {
      console.error('Error fetching coins list:', error);
    });
}
document.addEventListener('DOMContentLoaded', getUserBalance);

function getUserBalance() {
  // Make a GET request to the API endpoint for fetching user balance
  fetch('http://wafer.revs.ir/api/balance?username=aliu')
    .then(response => response.json())
    .then(data => {
      const balanceElement = document.getElementById('balance');
      balanceElement.textContent = `${data.blu} BluCoins`;
    })
    .catch(error => {
      console.error('Error:', error);
      const balanceElement = document.getElementById('balance');
      balanceElement.textContent = 'Error occurred while fetching balance.';
    });
}
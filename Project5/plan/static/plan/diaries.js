document.addEventListener('DOMContentLoaded', () => {

    // default is date search, hide mood search
    document.querySelector('#mood-search-view').style.display = 'none';

    // Add eventlistener to listen for 'change'
    document.querySelector('#search-select').addEventListener('change', () => {
        const select = document.querySelector('#search-select').value;
        if (select === 'date') {
            // show date search, hide mood search 
            document.querySelector('#date-search-view').style.display = 'block';
            document.querySelector('#mood-search-view').style.display = 'none';
        } else if (select === 'mood') {
            // do opposite
            document.querySelector('#date-search-view').style.display = 'none';
            document.querySelector('#mood-search-view').style.display = 'block';
        }
    });

})


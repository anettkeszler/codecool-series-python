const genreCards = document.querySelectorAll('#genre-id')
genreCards.forEach( card => card.addEventListener('dblclick', function (){
    // console.log(typeof this.dataset.shows);
    const number = parseInt(this.dataset.shows);
    console.log(typeof number)
    if (number % 2 === 0) {
        this.classList.add('even')
    } else {
        this.classList.add('odd')
    }

}))





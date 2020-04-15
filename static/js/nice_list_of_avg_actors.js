const ratings = document.querySelectorAll('.rating')


function leftClickEvent() {
    ratings.forEach(rating => {
        rating.addEventListener('click', function() {
            console.log(rating.textContent);
            console.log(typeof(rating.textContent));
            let intRatingValueLeft = Number(rating.textContent);
            console.log(typeof(intRatingValueLeft));
            intRatingValueLeft += 0.1;
            rating.innerText = intRatingValueLeft.toFixed(2);


        })
    })
}

leftClickEvent();


function rightClickEvent() {
    ratings.forEach(rating => {
        rating.addEventListener('contextmenu', function () {
            let intRatingValueRight = Number(rating.textContent);
            intRatingValueRight -= 0.1;
            rating.innerText = intRatingValueRight.toFixed(2);
        } )
    })
}
rightClickEvent();
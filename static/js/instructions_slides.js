'use strict'

const instructions = [
  '<p>“Please try again” is a two-player game. One player serves as the CONTENT PROVIDER. The other player takes on the role of the CONTENT MODERATOR.</p>\n<p>The CONTENT PROVIDER’s job is to submit content based on a shown prompt.</p>\n<p>The CONTENT MODERATOR determines whether the submitted content is accepted or rejected based on the rule shown on a rule card.</p>',
  '<p>The content provider will not be told this rule. Every time a piece of content is rejected, the content moderator may provide a hint about the rule, without giving the rule away. The content provider can try as many times as they want to get a piece of content accepted. The aim is to get a piece of content accepted in as few attempts as possible.</p>\n<p>What did you eat for lunch?</p>\n<p>How much money is in the jackpot at the end of the rainbow?</p>\n<p>What’s the temperature of the room?</p>',
  '<p>The content moderator can disclose what the rule is when either a) the content provider decides to give up and skip this round, b) the content provider guesses the rule correctly, or c) a piece of content is accepted and the content provider gives up in guessing what the rule was.</p>\n<p>Prompt: How much money is in the jackpot at the end of the rainbow? Rule: Input has to end in three zeros</p>\n<p>Hover over me for extra help during the game  :)</p>'
]

function prevSlide () {
  let prevButton = document.getElementById('previous-slide-button')
  let prevSlideNum = parseInt(prevButton.getAttribute('value'))
  let newText = instructions[prevSlideNum]

  let introHowTo = document.getElementById('how-to-play')
  introHowTo.innerHTML = newText

  if (prevSlideNum == 0) {
    // Hide previous slide button if going to the first slide
    prevButton.style.display = 'none'
  }

  // Update previous button value
  prevButton.setAttribute('value', prevSlideNum - 1)

  // Update next button value
  let nextButton = document.getElementById('next-slide-button')
  let currNextSlideNum = parseInt(nextButton.getAttribute('value'))
  nextButton.setAttribute('value', currNextSlideNum - 1)

  if (nextButton.style.display == 'none') {
    // Show next slide button
    nextButton.style.display = 'block'
  }
}

function nextSlide () {
  let nextButton = document.getElementById('next-slide-button')
  let nextSlideNum = parseInt(nextButton.getAttribute('value'))

  if (nextSlideNum == instructions.length) {
    // If on last intro slide, clicking the next arrow starts the game by going to the set up game page
    location.href = '/setup'
    return
  }

  let newText = instructions[nextSlideNum]

  let introHowTo = document.getElementById('how-to-play')
  introHowTo.innerHTML = newText

  if (nextSlideNum == instructions.length) {
    // Hide next slide button if going to the last slide
    nextButton.style.display = 'none'
  }

  // Update next button value
  nextButton.setAttribute('value', nextSlideNum + 1)
  console.log('nextSlideNum: ' + nextSlideNum)
  console.log('+1: ' + (nextSlideNum + 1))

  // Update previous button value
  let prevButton = document.getElementById('previous-slide-button')
  let currPrevSlideNum = parseInt(prevButton.getAttribute('value'))
  prevButton.setAttribute('value', currPrevSlideNum + 1)

  if (prevButton.style.display == 'none') {
    // Show previous slide button
    prevButton.style.display = 'block'
  }
}

const quizData = [
    {
      question: 'What year was Pokemon first founded?',
      options: ['1999', '1992', '1997', '1996'],
      answer: '1996',
    },
    {
      question: 'What is the newest pokemon set of this year?',
      options: ['Scarlet & Violet: Paldea Evolved',
      'Scarlet & Violet: Paradox Rift',
      'Scarlet & Violet: 151',
      'Scarlet & Violet: Obsidian Flame',
    ],
      answer: 'Scarlet & Violet: Paradox Rift',
    },
    {
      question: 'What is the maximum number of Pokemon a player can carry in their party?',
      options: ['5', '7', '8', '6'],
      answer: '6',
    },
    {
      question: 'Which Pokemon type is strong against Fire-type moves?',
      options: ['Water', 'Electric', 'Psychic', 'Dark'],
      answer: 'Water',
    },
    {
      question: 'How many Pokemon types exist in total?',
      options: ['17', '19', '21', '18'],
      answer: '18',
    },
    {
      question: 'What is the first Pokemon ever created?',
      options: ['Rhydon', 'Pikachu', 'Charmander', 'Mew'],
      answer: 'Rhydon',
    },
    {
      question: 'What is the name of the region in the Pokemon Gold and Silver games?',
      options: ['Johto', 'Kanto', 'Hoenn', 'Sinnoh'],
      answer: 'Johto',
    },
    {
      question: 'What is the signature move of the Pokemon Charizard?',
      options: ['Sacred Fire', 'Flamethrower', 'Fire Blast', 'Fire Fist'],
      answer: 'Flamethrower',
    },
    {
      question: 'Who is Ash Ketchums main rival in the Pokemon anime series?',
      options: ['Gary', 'Paul', 'Alain', 'Leon'],
      answer: 'Gary',
    },
    {
      question: 'Which Pokemon is known as the "Master of Illusions"?',
      options: ['Ditto', 'Zoroark', 'Mimikyu', 'Duplica'],
      answer: 'Zoroark',
    },
  ];

  const quizContainer = document.getElementById('quiz');
  const resultContainer = document.getElementById('result');
  const submitButton = document.getElementById('submit');
  const retryButton = document.getElementById('retry');
  const showAnswerButton = document.getElementById('showAnswer');
  const saveAnswerButton = document.getElementById('saveAnswer');


  let currentQuestion = 0;
  let score = 0;
  let incorrectAnswers = [];

  function getScore() {
    return score;
  }

  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }

  function displayQuestion() {
    const questionData = quizData[currentQuestion];

    const questionElement = document.createElement('div');
    questionElement.className = 'question';
    questionElement.innerHTML = questionData.question;

    const optionsElement = document.createElement('div');
    optionsElement.className = 'options';

    const shuffledOptions = [...questionData.options];
    shuffleArray(shuffledOptions);

    for (let i = 0; i < shuffledOptions.length; i++) {
      const option = document.createElement('label');
      option.className = 'option';

      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = 'quiz';
      radio.value = shuffledOptions[i];

      const optionText = document.createTextNode(shuffledOptions[i]);

      option.appendChild(radio);
      option.appendChild(optionText);
      optionsElement.appendChild(option);
    }

    quizContainer.innerHTML = '';
    quizContainer.appendChild(questionElement);
    quizContainer.appendChild(optionsElement);
  }

  function checkAnswer() {
    const selectedOption = document.querySelector('input[name="quiz"]:checked');
    if (selectedOption) {
      const answer = selectedOption.value;
      if (answer === quizData[currentQuestion].answer) {
        score++;
      } else {
        incorrectAnswers.push({
          question: quizData[currentQuestion].question,
          incorrectAnswer: answer,
          correctAnswer: quizData[currentQuestion].answer,
        });
      }
      currentQuestion++;
      selectedOption.checked = false;
      if (currentQuestion < quizData.length) {
        displayQuestion();
      } else {
        displayResult();
      }
    }
  }

  function displayResult() {
    quizContainer.style.display = 'none';
    submitButton.style.display = 'none';
    retryButton.style.display = 'inline-block';
    showAnswerButton.style.display = 'inline-block';
    saveAnswerButton.style.display = 'inline-block';
    resultContainer.innerHTML = `You scored ${score} out of ${quizData.length}!`;
  }

  function retryQuiz() {
    currentQuestion = 0;
    score = 0;
    incorrectAnswers = [];
    quizContainer.style.display = 'block';
    submitButton.style.display = 'inline-block';
    retryButton.style.display = 'none';
    showAnswerButton.style.display = 'none';
    resultContainer.innerHTML = '';
    displayQuestion();
  }

  function showAnswer() {
    quizContainer.style.display = 'none';
    submitButton.style.display = 'none';
    retryButton.style.display = 'inline-block';
    showAnswerButton.style.display = 'none';

    let incorrectAnswersHtml = '';
    for (let i = 0; i < incorrectAnswers.length; i++) {
      incorrectAnswersHtml += `
        <p>
          <strong>Question:</strong> ${incorrectAnswers[i].question}<br>
          <strong>Your Answer:</strong> ${incorrectAnswers[i].incorrectAnswer}<br>
          <strong>Correct Answer:</strong> ${incorrectAnswers[i].correctAnswer}
        </p>
      `;
    }

    resultContainer.innerHTML = `
      <p>You scored ${score} out of ${quizData.length}!</p>
      <p>Incorrect Answers:</p>
      ${incorrectAnswersHtml}
    `;
  }

  submitButton.addEventListener('click', checkAnswer);
  retryButton.addEventListener('click', retryQuiz);
  showAnswerButton.addEventListener('click', showAnswer);

  displayQuestion();
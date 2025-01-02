import React, { useState, useEffect, useCallback } from 'react';

const DIFFICULTY_SETTINGS = {
  easy: {
    GRAVITY: 0.4,
    JUMP_FORCE: -8,
    PIPE_SPEED: 2,
    PIPE_SPAWN_RATE: 2000,
    PIPE_GAP: 180,
    COLOR: 'bg-green-500'
  },
  medium: {
    GRAVITY: 0.6,
    JUMP_FORCE: -10,
    PIPE_SPEED: 3,
    PIPE_SPAWN_RATE: 1500,
    PIPE_GAP: 140,
    COLOR: 'bg-yellow-500'
  },
  hard: {
    GRAVITY: 0.8,
    JUMP_FORCE: -11,
    PIPE_SPEED: 4,
    PIPE_SPAWN_RATE: 1200,
    PIPE_GAP: 120,
    COLOR: 'bg-red-500'
  }
};

const Bird = ({ rotation, position }) => (
  <div
    className="absolute w-8 h-8"
    style={{
      top: position,
      left: 50,
      transform: `rotate(${rotation}deg)`,
      transition: 'transform 0.1s',
    }}
  >
    <div className="relative w-full h-full">
      <div className="absolute w-4 h-3 bg-yellow-400 rounded-full" 
        style={{ 
          top: '60%', 
          left: '25%',
          animation: 'flapWings 0.3s infinite alternate'
        }} 
      />
      <div className="absolute w-8 h-6 bg-yellow-400 rounded-full" />
      <div className="absolute w-3 h-3 bg-white rounded-full" style={{ top: '20%', left: '60%' }}>
        <div className="absolute w-1.5 h-1.5 bg-black rounded-full" style={{ top: '25%', left: '25%' }} />
      </div>
      <div className="absolute w-4 h-3 bg-orange-500 rounded" style={{ top: '40%', left: '75%' }} />
    </div>
  </div>
);

const Ground = ({ position }) => (
  <div 
    className="absolute bottom-0 w-[800px] h-20 bg-green-800"
    style={{ 
      left: position,
      backgroundImage: `
        linear-gradient(to bottom, 
          #a7d129 0%, #a7d129 20%, 
          #7c9927 20%, #7c9927 40%,
          #5c721d 40%, #5c721d 60%,
          #3f4f14 60%, #3f4f14 100%)
      `
    }}
  />
);

const DifficultySelector = ({ onSelect }) => (
  <div className="flex flex-col items-center gap-4">
    <h2 className="text-3xl font-bold text-white mb-4">Select Difficulty</h2>
    <button
      onClick={() => onSelect('easy')}
      className="w-48 px-6 py-3 bg-green-500 text-white rounded-lg text-xl font-bold hover:bg-green-600 transform hover:scale-105 transition-all"
    >
      Easy
    </button>
    <button
      onClick={() => onSelect('medium')}
      className="w-48 px-6 py-3 bg-yellow-500 text-white rounded-lg text-xl font-bold hover:bg-yellow-600 transform hover:scale-105 transition-all"
    >
      Medium
    </button>
    <button
      onClick={() => onSelect('hard')}
      className="w-48 px-6 py-3 bg-red-500 text-white rounded-lg text-xl font-bold hover:bg-red-600 transform hover:scale-105 transition-all"
    >
      Hard
    </button>
  </div>
);

const FlappyBird = () => {
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(0);
  const [birdPosition, setBirdPosition] = useState(250);
  const [birdVelocity, setBirdVelocity] = useState(0);
  const [pipes, setPipes] = useState([]);
  const [groundPos, setGroundPos] = useState(0);
  const [difficulty, setDifficulty] = useState(null);
  
  const settings = difficulty ? DIFFICULTY_SETTINGS[difficulty] : DIFFICULTY_SETTINGS.medium;
  const PIPE_WIDTH = 52;
  
  useEffect(() => {
    if (!gameStarted || gameOver || !difficulty) return;
    
    const gameLoop = setInterval(() => {
      setBirdPosition(pos => {
        const newPos = pos + birdVelocity;
        if (newPos > 460 || newPos < 0) {
          setGameOver(true);
          return pos;
        }
        return newPos;
      });
      
      setBirdVelocity(vel => vel + settings.GRAVITY);
      setGroundPos(pos => (pos - settings.PIPE_SPEED) % -30);
      
      setPipes(currentPipes => {
        return currentPipes
          .map(pipe => ({
            ...pipe,
            x: pipe.x - settings.PIPE_SPEED
          }))
          .filter(pipe => pipe.x > -60);
      });
      
      pipes.forEach(pipe => {
        const birdBox = {
          left: 50,
          right: 82,
          top: birdPosition,
          bottom: birdPosition + 32
        };
        
        const topPipeBox = {
          left: pipe.x,
          right: pipe.x + PIPE_WIDTH,
          top: 0,
          bottom: pipe.height
        };
        
        const bottomPipeBox = {
          left: pipe.x,
          right: pipe.x + PIPE_WIDTH,
          top: pipe.height + settings.PIPE_GAP,
          bottom: 500
        };
        
        if (
          (birdBox.right > topPipeBox.left && 
           birdBox.left < topPipeBox.right && 
           birdBox.top < topPipeBox.bottom) ||
          (birdBox.right > bottomPipeBox.left && 
           birdBox.left < bottomPipeBox.right && 
           birdBox.bottom > bottomPipeBox.top)
        ) {
          setGameOver(true);
        }
        
        if (pipe.x === 48) {
          const newScore = score + 1;
          setScore(newScore);
          if (newScore > highScore) {
            setHighScore(newScore);
          }
        }
      });
    }, 16);
    
    return () => clearInterval(gameLoop);
  }, [gameStarted, gameOver, birdPosition, birdVelocity, pipes, difficulty, settings, score, highScore]);
  
  useEffect(() => {
    if (!gameStarted || gameOver || !difficulty) return;
    
    const spawnPipe = setInterval(() => {
      const height = Math.floor(Math.random() * (300 - 100) + 100);
      setPipes(currentPipes => [...currentPipes, { x: 400, height }]);
    }, settings.PIPE_SPAWN_RATE);
    
    return () => clearInterval(spawnPipe);
  }, [gameStarted, gameOver, difficulty, settings]);
  
  const handleJump = useCallback(() => {
    if (!difficulty) return;
    if (!gameStarted) {
      setGameStarted(true);
    }
    if (!gameOver) {
      setBirdVelocity(settings.JUMP_FORCE);
    }
  }, [gameStarted, gameOver, difficulty, settings]);
  
  const handleRestart = () => {
    setGameStarted(false);
    setGameOver(false);
    setScore(0);
    setBirdPosition(250);
    setBirdVelocity(0);
    setPipes([]);
    setDifficulty(null);
  };

  const selectDifficulty = (diff) => {
    setDifficulty(diff);
    setGameStarted(false);
    setGameOver(false);
    setScore(0);
    setBirdPosition(250);
    setBirdVelocity(0);
    setPipes([]);
  };

  return (
    <div 
      className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-300 to-blue-500"
      onClick={difficulty ? handleJump : undefined}
    >
      <div className="relative w-96 h-[500px] bg-gradient-to-b from-blue-200 to-blue-400 overflow-hidden">
        <Bird rotation={birdVelocity * 3} position={birdPosition} />
        
        {pipes.map((pipe, index) => (
          <React.Fragment key={index}>
            <div
              className="absolute"
              style={{
                left: pipe.x,
                width: PIPE_WIDTH,
                height: pipe.height,
                top: 0,
              }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-green-700 via-green-600 to-green-700 border-l-4 border-r-4 border-green-900" />
              <div 
                className="absolute left-[-8px] right-[-8px] h-12 bg-gradient-to-r from-green-800 via-green-700 to-green-800 border-4 border-green-900 rounded-sm"
                style={{ bottom: 0 }}
              />
            </div>
            <div
              className="absolute"
              style={{
                left: pipe.x,
                width: PIPE_WIDTH,
                top: pipe.height + settings.PIPE_GAP,
                bottom: 0,
              }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-green-700 via-green-600 to-green-700 border-l-4 border-r-4 border-green-900" />
              <div 
                className="absolute left-[-8px] right-[-8px] h-12 bg-gradient-to-r from-green-800 via-green-700 to-green-800 border-4 border-green-900 rounded-sm"
                style={{ top: 0 }}
              />
            </div>
          </React.Fragment>
        ))}
        
        <Ground position={groundPos} />
        <Ground position={groundPos + 400} />
        
        {difficulty && (
          <div className="absolute top-4 left-1/2 transform -translate-x-1/2 text-6xl font-bold text-white drop-shadow-lg">
            {score}
          </div>
        )}
        
        {!difficulty ? (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <DifficultySelector onSelect={selectDifficulty} />
          </div>
        ) : !gameStarted && !gameOver ? (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className={`text-white text-2xl font-bold text-center px-4 py-3 ${DIFFICULTY_SETTINGS[difficulty].COLOR} rounded-lg transform hover:scale-105 transition-transform`}>
              Tap to Start
            </div>
          </div>
        ) : null}
        
        {gameOver && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-6 text-center">
              <div className="text-4xl font-bold mb-4">Game Over!</div>
              <div className="text-2xl mb-2">Score: {score}</div>
              <div className="text-xl mb-6">High Score: {highScore}</div>
              <div className="flex flex-col gap-3">
                <button
                  className={`px-6 py-3 text-white rounded-lg text-xl font-bold transform hover:scale-105 transition-all ${DIFFICULTY_SETTINGS[difficulty].COLOR}`}
                  onClick={() => selectDifficulty(difficulty)}
                >
                  Retry
                </button>
                <button
                  className="px-6 py-3 bg-blue-500 text-white rounded-lg text-xl font-bold hover:bg-blue-600 transform hover:scale-105 transition-all"
                  onClick={handleRestart}
                >
                  Change Difficulty
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
      
      <style jsx>{`
        @keyframes flapWings {
          from { transform: translateY(0); }
          to { transform: translateY(-4px); }
        }
      `}</style>
    </div>
  );
};

export default FlappyBird;

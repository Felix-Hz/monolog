$(document).ready(function () {
    const walkingFrames = [
        `    /\\_/\\
     ( o.o )
      > ^ <
     /|   |\\
    (_|   |_)`,
        `    /\\_/\\
     ( o.o )
      > ^ <
      |   |\\
     _|   |_)`,
        `    /\\_/\\
     ( -.- )
      > ^ <
     /|   |
    (_|   |_`,
        `    /\\_/\\
     ( o.o )
      > ^ <
     /|   |
     (|   |_)`,
        `    /\\_/\\
     ( ^.^ )
      > w <
     /|   |\\
    (_|   |_)`,
    ];

    let currentFrame = 0;
    setInterval(() => {
        $(".walking-cat").text(walkingFrames[currentFrame]);
        currentFrame = (currentFrame + 1) % walkingFrames.length;
    }, 400);
});

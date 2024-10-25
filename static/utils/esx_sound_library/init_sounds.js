const startSoundPlayer = (sound_path = "") => {
    var soundManager = new Audio(sound_path);
    soundManager.play();
}
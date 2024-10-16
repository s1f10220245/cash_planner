function openPopup() {
    const width = 600;
    const height = 400;
    const left = (window.screen.width / 2) - (width / 2);
    const top = (window.screen.height / 2) - (height / 2);
    window.open("{% url 'add_expense' %}", 'ポップアップ', 
                `width=${width},height=${height},top=${top},left=${left}`);
}

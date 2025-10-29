// aiChat
const form = document.getElementById('aiForm');
const textarea = document.getElementById('question');
const error = document.getElementById('error');
form.addEventListener('submit', function(event) {
        const value = textarea.value.trim();
        if (value === "") {
            error.style.display = 'inline';
            event.preventDefault(); // フォーム送信を止める
        } else {
            error.style.display = 'none';
        }
    }

);
// 入力中にエラーを消す
textarea.addEventListener('input', function() {
        if (textarea.value.trim() !== "") {
            error.style.display = 'none';
        }
    }

);
// 成長グラフ
const data = JSON.parse(document.getElementById('growth-chart-data').textContent);
const ctx = document.getElementById('growthChart').getContext('2d');
const growthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: '身長(cm)',
                data: data.height_data,
                borderColor: 'blue',
                fill: false
            }, {
                label: '体重(kg)',
                data: data.weight_data,
                borderColor: 'green',
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    }

);

function showForm(category) {
    // 全フォームを非表示にし、requiredを解除
    document.querySelectorAll('.record-form').forEach(el => {
        el.classList.add('d-none');
        el.querySelectorAll('[required]').forEach(input => {
            input.dataset.wasRequired = "true"; // 元々requiredだったか記録
            input.removeAttribute('required');
        });
    });
    // 選択フォームを表示してrequiredを復活
    const activeForm = document.getElementById('form-' + category);
    if (activeForm) {
        activeForm.classList.remove('d-none');
        activeForm.querySelectorAll('[data-was-required]').forEach(input => {
            input.setAttribute('required', true);
        });
    }
}
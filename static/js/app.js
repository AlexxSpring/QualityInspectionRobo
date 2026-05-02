document.addEventListener('DOMContentLoaded', () => {
    
    // Elements
    const valWeight = document.getElementById('val-weight');
    const valDistance = document.getElementById('val-distance');
    const valIr = document.getElementById('val-ir');
    
    const progWeight = document.getElementById('prog-weight');
    const progDist = document.getElementById('prog-dist');
    
    const qualityStatus = document.getElementById('quality-status');
    const qualityDetails = document.getElementById('quality-details');
    
    const btnServo = document.getElementById('btn-servo');
    const btnLight = document.getElementById('btn-light');

    // Polling Interval
    const POLLING_RATE = 1000; // 1 second

    // Fetch Sensor Data
    async function fetchSensors() {
        try {
            const res = await fetch('/api/sensors');
            if (!res.ok) throw new Error('Network response was not ok');
            const data = await res.json();
            
            // Update Text
            valWeight.innerText = `${data.weight_kg.toFixed(2)} kg`;
            valDistance.innerText = `${data.distance_cm.toFixed(1)} cm`;
            valIr.innerText = data.ir_object_detected ? 'DETECTED' : 'CLEAR';
            
            // Update Progress Bars (Visual representation)
            // Weight range assumed 0-5kg for bar
            const weightPercent = Math.min(100, Math.max(0, (data.weight_kg / 5.0) * 100));
            progWeight.style.width = `${weightPercent}%`;
            
            // Distance range assumed 0-50cm for bar
            const distPercent = Math.min(100, Math.max(0, (data.distance_cm / 50.0) * 100));
            progDist.style.width = `${distPercent}%`;

        } catch (error) {
            console.error("Error fetching sensor data:", error);
        }
    }

    // Fetch Quality Data
    async function fetchQuality() {
        try {
            const res = await fetch('/api/quality/check', { method: 'POST' });
            if (!res.ok) throw new Error('Network response was not ok');
            const data = await res.json();
            
            // Update UI
            if (data.is_pass) {
                qualityStatus.className = 'status-badge pass';
                qualityStatus.innerHTML = '<i class="fa-solid fa-check-circle"></i> PASS';
            } else {
                qualityStatus.className = 'status-badge fail';
                qualityStatus.innerHTML = '<i class="fa-solid fa-times-circle"></i> FAIL';
            }
            qualityDetails.innerText = data.details;

        } catch (error) {
            console.error("Error fetching quality data:", error);
            qualityStatus.className = 'status-badge';
            qualityStatus.innerHTML = '<i class="fa-solid fa-exclamation-triangle"></i> ERROR';
            qualityDetails.innerText = "Connection lost.";
        }
    }

    // Controls
    btnServo.addEventListener('click', async () => {
        const btn = btnServo;
        const origHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cycling...';
        btn.disabled = true;
        
        try {
            await fetch('/api/control/servo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ angle: 90 })
            });
        } catch(e) {
            console.error(e);
        } finally {
            setTimeout(() => {
                btn.innerHTML = origHtml;
                btn.disabled = false;
            }, 1000);
        }
    });

    btnLight.addEventListener('click', async () => {
        try {
            await fetch('/api/control/light', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ state: 'TOGGLE', brightness: 100 })
            });
        } catch(e) {
            console.error(e);
        }
    });

    // Start Polling
    setInterval(() => {
        fetchSensors();
        fetchQuality();
    }, POLLING_RATE);
    
    // Initial fetch
    fetchSensors();
    fetchQuality();
});

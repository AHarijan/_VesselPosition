var today = new Date()
const year = today.getFullYear();
const month = String(today.getMonth() +1).padStart(2,'0');
const day = String(today.getDate()).padStart(2,'0');

const currtDate = `${year}-${month}-${day}`;
document.getElementById('currentDate').value=currtDate;

const hours = String(today.getHours()).padStart(2, '0');
const minutes = String(today.getMinutes()).padStart(2, '0');
const currtDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
document.getElementById('currentDateTime').value = currtDateTime;

const currtStatus = "Expected"
document.getElementById('CurrStatus').value=currtStatus;


function lineUpForm(){

    const Port = document.getElementById('port').value
    const Berth = document.getElementById('berth').value
    const Imo = document.getElementById('imono').value
    const VesselSlt = document.getElementById('vesselSlt').value
    const Vessel = document.getElementById('vessel').value
    const Loa = document.getElementById('loa').value
    const Beam = document.getElementById('beam').value
    const Draft = document.getElementById('draft').value
    const Cargo1 = document.getElementById('cargo1').value
    const CargoQtyF1 = document.getElementById('cargoQtyF1').value
    const cargoQtyUnits1 = document.getElementById('cargoQtyU1').value
    const vesselType = document.getElementById('vesseltype').value
    const Operation = document.getElementById('operation').value
    const CoatForn = document.getElementById('cos/for').value
    const etaDate = document.getElementById('etadate').value;
    const etaTime = document.getElementById('etatime').value;
    const etbDate = document.getElementById('etbdate').value;
    const etbTime = document.getElementById('etbtime').value;
    const etcDate = document.getElementById('etcdate').value;
    const etcTime = document.getElementById('etctime').value;
    const lastport = document.getElementById('lastport').value
    const nextport = document.getElementById('nextport').value
    const agent = document.getElementById('agent').value
    const CurrentStatus = document.getElementById('CurrStatus').value;

    const eta = etaDate + " " + etaTime;
    const etb = etbDate + " " + etbTime;
    const etc = etcDate + " " + etcTime;

    let etaDateTime = eta.trim();
    let etbDateTime = etb.trim();
    let etcDateTime = etc.trim();

    let currDate = new Date();
    let etaDateTimeObj = new Date(etaDateTime);
    let etbDateTimeObj = new Date(etbDateTime);
    let etcDateTimeObj = new Date(etcDateTime);

    if (Port ===  "") {
        alert("Port cannot be kept blank");
        return false;
    } 
    else if (Berth ===  "") {
        alert("Berth cannot be kept blank");
        return false;
    } 
    else if (Imo ===  "") {
        alert("Imo cannot be kept blank");
        return false;
    }
    else if (VesselSlt === "") {
        alert("Vessel Slt cannot be kept blank");
        return false;
    } 
    else if (Vessel === "") {
        alert("Vessel Name cannot be kept blank");
        return false;
    }
    else if (Loa === "") {
        alert("LOA cannot be kept blank");
        return false;
    }
    else if (Beam === "") {
        alert("Beam Name cannot be kept blank");
        return false;
    }
    else if (Draft === "") {
        alert("Draft cannot be kept blank");
        return false;
    }
    
    
    if (CurrentStatus === "Expected") {
        let etaNotNull = !etaDate;
        let date_currD = etaDateTimeObj < currDate;
        if (date_currD || etaNotNull) {
            alert(`When the vessel is ${CurrentStatus}:
            Arrival Date cannot be blank or a past date`);
            return false;
        }
        
    } else if (CurrentStatus === "Arrived") {
        let ataNotBlank_A = !etaDateTime.includes(" ");
        let etbNotNull = !etbDate;
        let ata_etb = etaDateTimeObj > etbDateTimeObj;
        if (ataNotBlank_A || etbNotNull || ata_etb) {
            alert(`When the vessel is ${CurrentStatus}: 
            Arrival Date & Time cannot be blank or future date. 
            Berthing Date cannot be blank or before ETA.`); 
            return false;
        }
    } else if (CurrentStatus === "At Berth") {
        let ataNotNull_B  = !etaDate;
        let etbNotNull_B = !etbDate;
        let etcNotNull = !etcDate;
        let ataNotBlank_B = !etaDateTime.includes(" ");
        let atbNotBlank_B = !etbDateTime.includes(" ");
        let ata_etb_B = etaDateTimeObj > etbDateTimeObj;
        let atb_etc = etbDateTimeObj > etcDateTimeObj;
        if (ataNotNull_B || etbNotNull_B || etcNotNull || ataNotBlank_B || atbNotBlank_B || atb_etc || ata_etb_B) {
            alert(`When the vessel is ${CurrentStatus}: 
            Arrival Date & Time cannot be blank or future date. 
            Berthing Date & Time cannot be blank or before Arrival Date.
            Depature Date cannot be blank or before Berthing Date`); 
            return false;
        }
    } else if (CurrentStatus === "Sailed") {
        let ataNotNull_B  = !etaDate;
        let etbNotNull_B = !etbDate;
        let etcNotNull = !etcDate;
        let ataNotBlank_B = !etaDateTime.includes(" ");
        let atbNotBlank_B = !etbDateTime.includes(" ");
        let atcNotBlank_B = !etcDateTime.includes(" ");
        let ata_etb_B = etaDateTimeObj > etbDateTimeObj;
        let atb_etc = etbDateTimeObj > etcDateTimeObj;
        let lastportF = lastport.trim() !== "";
        let nextportF = nextport.trim() !== "";
        let agentF = agent.trim() !== "";
        if (ataNotNull_B || etbNotNull_B || etcNotNull || ataNotBlank_B || atbNotBlank_B || atcNotBlank_B || atb_etc || ata_etb_B || !lastportF || !nextportF || !agentF) {
            alert(`When the vessel is ${CurrentStatus}: 
            Arrival Date & Time cannot be blank or future date. 
            Berthing Date & Time cannot be blank or before Arrival Date.
            Depature Date & Time cannot be blank or before Berthing Date
            Last Port cannot be blank
            Next Port cannot be blank
            Agent cannot be blank`); 
            return false;
        }
    } 
    
    if (Cargo1 ===  "") {
        alert("First Cargo cannot be kept blank");
        return false;
    } 
    else if (isNaN(CargoQtyF1) || CargoQtyF1 === "") {
        alert("Quantity for First Cargo cannot be kept blank and accepts only numbers");
        return false;
    } 
    else if (cargoQtyUnits1 ===  "") {
        alert("Unit for First Cargo cannot be kept blank");
        return false;
    } 
    else if (vesselType ===  "") {
        alert("Vessel Type cannot be kept blank");
        return false;
    } 
    else if (Operation ===  "") {
        alert("Please select the operation type");
        return false;
    } 
    else if (CoatForn ===  "") {
        alert("Please mention if vessel is coastal or foreign");
        return false;
    } 
    else if (CurrentStatus.trim() === "") {
        alert("Please fill in the form, select the current status and SUBMIT again");
        return false;
    } 
    else 
    alert("Details submitted successfully")
    return true 
    
}

function cargo2() {
    const CargoQtyF2 = document.getElementById('cargoQtyF1').value
    const CargoQtyF3 = document.getElementById('cargoQtyF1').value

    if (CargoQtyF2 === "") {
        document.getElementById('cargoqty2').value = 0;
    }

    return true; 
}


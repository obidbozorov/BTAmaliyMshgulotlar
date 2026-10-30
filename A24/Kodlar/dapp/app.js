// A24 · DApp mantiqi: hamyon (MetaMask) → RPC → smart-kontrakt. ethers.js v6
const C = window.DAPP_CONFIG;
const $ = (id) => document.getElementById(id);
let provider, signer, kontrakt, decimals = 18n, belgi = "";
const korilgan = new Set();                                               // bir log ikki marta chiqmasin

function holat(matn, tur = "") {
  $("holat").className = tur;
  $("holat").innerHTML = matn;
}

function xatoMatni(e) {
  if (e?.code === "ACTION_REJECTED" || e?.code === 4001) return "Foydalanuvchi MetaMask'da rad etdi.";
  if (e?.reason) return "Kontrakt rad etdi: " + e.reason;                 // require(…, "matn")
  if (e?.shortMessage) return e.shortMessage;
  return e?.message || String(e);
}

const qisqa = (a) => a.slice(0, 6) + "…" + a.slice(-4);
const txHavola = (h) => `<a href="${C.TARMOQ.explorer}/tx/${h}" target="_blank" rel="noopener">${qisqa(h)}</a>`;

async function tarmoqniTekshir() {
  const { chainId } = await provider.getNetwork();
  $("tarmoq").textContent = "Tarmoq: " + chainId;
  if (chainId === BigInt(C.TARMOQ.chainId)) return true;
  try {                                                                    // A5 dagi wallet_switchEthereumChain
    await window.ethereum.request({ method: "wallet_switchEthereumChain", params: [{ chainId: "0x" + C.TARMOQ.chainId.toString(16) }] });
    return false;                                                          // chainChanged sahifani qayta yuklaydi
  } catch (e) {
    holat(`Noto'g'ri tarmoq (${chainId}). MetaMask'da ${C.TARMOQ.nomi} ni tanlang.`, "xato");
    return false;
  }
}

async function malumotniYangila() {
  const men = await signer.getAddress();
  const [nom, jami, balans] = await Promise.all([kontrakt.name(), kontrakt.totalSupply(), kontrakt.balanceOf(men)]);
  $("token").textContent = `${nom} (${belgi})`;
  $("jami").textContent = ethers.formatUnits(jami, decimals) + " " + belgi;
  $("hisob").textContent = men;
  $("balans").textContent = ethers.formatUnits(balans, decimals) + " " + belgi;
}

function jurnalgaQosh(from, to, value, hash, indeks, boshiga = true) {
  if (korilgan.has(hash + ":" + indeks)) return;                          // tarix va jonli tinglovchi bir blokni ikki marta berishi mumkin
  korilgan.add(hash + ":" + indeks);
  const li = document.createElement("li");
  const turi = from === ethers.ZeroAddress ? "MINT" : to === ethers.ZeroAddress ? "BURN" : "→";
  li.innerHTML = `${qisqa(from)} ${turi} ${qisqa(to)} · <b>${ethers.formatUnits(value, decimals)} ${belgi}</b> · ${txHavola(hash)}`;
  const j = $("jurnal");
  if (j.firstElementChild?.textContent === "—") j.innerHTML = "";
  boshiga ? j.prepend(li) : j.append(li);
}

async function jurnalniYukla() {
  const oxirgi = await provider.getBlockNumber();
  const loglar = await kontrakt.queryFilter(kontrakt.filters.Transfer(), Math.max(0, oxirgi - 5000), oxirgi);
  $("jurnal").innerHTML = "<li>—</li>";
  for (const l of loglar.slice(-10).reverse()) jurnalgaQosh(l.args.from, l.args.to, l.args.value, l.transactionHash, l.index, false);
  kontrakt.on("Transfer", (from, to, value, ev) => {                     // yangi o'tkazmalarni jonli kuzatish
    jurnalgaQosh(from, to, value, ev.log.transactionHash, ev.log.index);
    malumotniYangila();
  });
}

async function ulash() {
  if (!window.ethereum) return holat("MetaMask topilmadi. Kengaytmani o'rnating (A5).", "xato");
  try {
    provider = new ethers.BrowserProvider(window.ethereum);
    await provider.send("eth_requestAccounts", []);
    if (!(await tarmoqniTekshir())) return;
    if ((await provider.getCode(C.KONTRAKT)) === "0x")
      return holat(`${C.KONTRAKT} manzilida kontrakt yo'q. config.js dagi KONTRAKT va tarmoqni tekshiring.`, "xato");
    signer = await provider.getSigner();
    kontrakt = new ethers.Contract(C.KONTRAKT, C.ABI, signer);
    [decimals, belgi] = await Promise.all([kontrakt.decimals(), kontrakt.symbol()]);
    $("manzil").innerHTML = `<a href="${C.TARMOQ.explorer}/address/${C.KONTRAKT}" target="_blank" rel="noopener">${C.KONTRAKT}</a>`;
    await malumotniYangila();
    await jurnalniYukla();
    $("ulash").textContent = qisqa(await signer.getAddress());
    $("yuborish").disabled = false;
    holat("Ulandi.", "ok");
  } catch (e) {
    holat(xatoMatni(e), "xato");
  }
}

async function yuborish() {
  const kimga = $("kimga").value.trim(), miqdor = $("miqdor").value.trim().replace(",", ".");
  if (!ethers.isAddress(kimga)) return holat("Oluvchi manzili noto'g'ri (EIP-55 — A5).", "xato");
  let qiymat;
  try { qiymat = ethers.parseUnits(miqdor, decimals); } catch { return holat("Miqdor noto'g'ri.", "xato"); }
  $("yuborish").disabled = true;
  try {
    await kontrakt.transfer.staticCall(kimga, qiymat);                     // avval sinab ko'ramiz: xato bo'lsa gaz sarflanmaydi
    holat("MetaMask'da tasdiqlang…");
    const tx = await kontrakt.transfer(kimga, qiymat);
    holat("Yuborildi, blokka tushishi kutilmoqda: " + txHavola(tx.hash));
    const r = await tx.wait();
    await malumotniYangila();                                              // avval balans, keyin xabar
    $("miqdor").value = "";
    holat(`Tasdiqlandi: blok #${r.blockNumber}, gaz ${r.gasUsed} · ${txHavola(tx.hash)}`, "ok");
  } catch (e) {
    holat(xatoMatni(e), "xato");
  } finally {
    $("yuborish").disabled = false;
  }
}

$("ulash").onclick = ulash;
$("yuborish").onclick = yuborish;
if (window.ethereum) {
  window.ethereum.on?.("accountsChanged", () => location.reload());
  window.ethereum.on?.("chainChanged", () => location.reload());
}

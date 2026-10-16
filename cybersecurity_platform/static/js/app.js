// Small client-side enhancements; security decisions remain server-side.
document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('table tbody tr').forEach(r=>r.addEventListener('click',()=>r.classList.add('table-active')))});

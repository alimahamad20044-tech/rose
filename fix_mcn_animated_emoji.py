# ────────────────────────────────────────────────────────────────────────────
# FIX: ئیمۆجی ئەنیمەیتد لە ئەنجامی تێستی MCN  (handlers.py)
#
# Root cause:
#   edit_message_text  →  ئیمۆجی custom emoji ئەنیمەیتد نانوێت (دیاری کراوە لە HBDI)
#   reply_text         →  ئیمۆجی ئەنیمەیتد دەخاتە کار  ✓
#
# پێش ئەم fix — پێشتر reply_text Document_invalid دەدا چونکە coroutine object
# ناو تێکستەکەدا دەچووە (BUG-CORO) و HTML خراپ دەکرد.  ئێستا _sanitize_coroutines
# ئەو coroutine ـە پاک دەکات پێش ناردنەوە، بۆیە reply_text ئێستا سەلامەتە.
#
# Change to make in handlers.py → function _mcn_show_result
# ────────────────────────────────────────────────────────────────────────────
#
# ── BEFORE (WRONG) ──────────────────────────────────────────────────────────
#
#     text = _sanitize_coroutines(text, "_mcn_show_result")  # FIX BUG-CORO
#     await _safe_edit(query, text, reply_markup=kb)
#
# ── AFTER (FIXED) ───────────────────────────────────────────────────────────
#
#     text = _sanitize_coroutines(text, "_mcn_show_result")  # FIX BUG-CORO
#     # ── ئیمۆجی ئەنیمەیتد پێویستی بە reply_text هەیە (نەک edit) ──
#     try:
#         await query.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
#         try:
#             await query.message.delete()
#         except Exception:
#             pass
#     except Exception as _te:
#         logger.error("_mcn_show_result reply_text: %s", _te)
#         await _safe_edit(query, text, reply_markup=kb)
#
# ────────────────────────────────────────────────────────────────────────────
# Same pattern used by _hbdi_show_result (which works correctly):
#
#     # ── ئیمۆجی ئەنیمەیتد پێویستی بە reply_text هەیە (نەک edit) ──
#     try:
#         await query.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
#         try:
#             await query.message.delete()
#         except Exception:
#             pass
#     except Exception as _te:
#         logger.error("_hbdi_show_result reply_text: %s", _te)
#         await _safe_edit(query, text, reply_markup=kb)
# ────────────────────────────────────────────────────────────────────────────

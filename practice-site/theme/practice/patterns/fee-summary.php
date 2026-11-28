<?php
/**
 * Title: Fee summary
 * Slug: practice/fee-summary
 * Categories: practice
 * Description: Places the shared fee blocks. Change a fee in Patterns, not here.
 */
?>
<!-- wp:group {"metadata":{"name":"Fee summary"},"style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|50"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group" style="padding-top:var(--wp--preset--spacing--40);padding-bottom:var(--wp--preset--spacing--50)">
<!-- wp:heading --><h2 class="wp-block-heading">What it costs</h2><!-- /wp:heading -->
<?php echo practice_synced( 'fee-standard-session' ); ?>
<!-- wp:paragraph --><p>You pay at the end of each session. If you need to cancel, [x] hours' notice means no fee. <span class="practice-draft">terms to confirm</span></p><!-- /wp:paragraph -->
<!-- wp:paragraph --><p><a href="/fees/">Fees, rebates and your first appointment</a></p><!-- /wp:paragraph -->
</div>
<!-- /wp:group -->

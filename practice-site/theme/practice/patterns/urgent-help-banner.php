<?php
/**
 * Title: Urgent help banner
 * Slug: practice/urgent-help-banner
 * Categories: practice
 * Description: Places the shared Urgent help block.
 */
?>
<!-- wp:group {"metadata":{"name":"Urgent help"},"className":"practice-urgent","backgroundColor":"surface","style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|40","left":"var:preset|spacing|40","right":"var:preset|spacing|40"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group practice-urgent has-surface-background-color has-background" style="padding:var(--wp--preset--spacing--40)">
<?php echo practice_synced( 'urgent-help' ); ?>
</div>
<!-- /wp:group -->

<?php
/*
Plugin Name: Digital Rust WordPress Plugin
Plugin URI:
Description: This plugin degrades WordPress posts at random over time
Version: 0.1a
Author: Steve Moss
Author URI: http://stevemoss.ath.cx/
License: GPLv3
*/

/*	
	Digital Rust - Degrades WordPress posts at random over time
    Copyright (C) 2012	Steve Moss (gawbul@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function digital_rust_init() {
	global $wpdb;	
	global $title_len, $content_len;
	
	// Get current post ID
	$this_id = get_the_ID();

	// Setup SELECT SQL query
	$sql = "SELECT ID, post_title, post_content
	FROM $wpdb->posts
	WHERE post_status = 'publish' AND ID <> $this_id
	ORDER BY RAND()
	LIMIT 1";
	
	// Get SQL results
	$posts = $wpdb->get_results($sql);

	// Set variables from SQL results
	$post_id = $posts[0]->ID;
	$post_title = $posts[0]->post_title;
	$post_content = $posts[0]->post_content;

	// Get length of post title and content
	$title_len = strlen($post_title);
	$content_len = strlen($post_content);
	
	// Set decay lens to 5% and 10%
	$decay_title_len = ceil($title_len / 100 * 5); // always round up
	$decay_content_len = round($content_len / 100 * 10); // use standard round
	
	// Decay title
	foreach(range(1, $decay_title_len) as $number):
		$rnd = rand(1, $title_len);
		$post_title = substr_replace($post_title, " ", $rnd, 1);
	endforeach;
	
	// Decay content
	foreach(range(1, $decay_content_len) as $number):
		$rnd = rand(1, $content_len);
		$post_content = substr_replace($post_content, " ", $rnd, 1);
	endforeach;

	// Update database
	$wpdb->update(
					$wpdb->posts,
					array(
							'post_title' =>	$post_title,
							'post_content' => $post_content,
					),
					array(	'ID' => $post_id),
					array(
							'%s',
							'%d'
					), 
					array('%d') 
	);
}

add_action('wp_footer', 'digital_rust_init');
?>
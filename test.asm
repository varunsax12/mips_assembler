loop: add $t1, $a0, $s0
	lb $t1, 0($t1)
	add $t2, $a1, $s0
	sb $t1, 0($t2)
	addi $s0, $s0, 1
	bne $t1, $0, loop
	lw $s0, 0($sp)
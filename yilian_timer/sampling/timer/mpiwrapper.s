	.text
	.file	"mpiwrapper.c"
	.globl	MPI_Init                # -- Begin function MPI_Init
	.p2align	4, 0x90
	.type	MPI_Init,@function
MPI_Init:                               # @MPI_Init
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$216, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movq	%rdi, %rbx
	movl	$0, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -48(%rbp)
	movq	%r14, -40(%rbp)
	movq	-48(%rbp), %rdi
	movq	-40(%rbp), %rsi
	callq	PMPI_Init
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_1, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$216, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	MPI_Init, .Lfunc_end0-MPI_Init
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Finalize            # -- Begin function MPI_Finalize
	.p2align	4, 0x90
	.type	MPI_Finalize,@function
MPI_Finalize:                           # @MPI_Finalize
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$208, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movl	$1, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	callq	PMPI_Finalize
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_2, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$208, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end1:
	.size	MPI_Finalize, .Lfunc_end1-MPI_Finalize
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Bsend               # -- Begin function MPI_Bsend
	.p2align	4, 0x90
	.type	MPI_Bsend,@function
MPI_Bsend:                              # @MPI_Bsend
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	$2, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	callq	PMPI_Bsend
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_3, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end2:
	.size	MPI_Bsend, .Lfunc_end2-MPI_Bsend
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Bsend_init          # -- Begin function MPI_Bsend_init
	.p2align	4, 0x90
	.type	MPI_Bsend_init,@function
MPI_Bsend_init:                         # @MPI_Bsend_init
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$3, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Bsend_init
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_4, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end3:
	.size	MPI_Bsend_init, .Lfunc_end3-MPI_Bsend_init
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Recv_init           # -- Begin function MPI_Recv_init
	.p2align	4, 0x90
	.type	MPI_Recv_init,@function
MPI_Recv_init:                          # @MPI_Recv_init
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$4, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Recv_init
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_5, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end4:
	.size	MPI_Recv_init, .Lfunc_end4-MPI_Recv_init
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Send_init           # -- Begin function MPI_Send_init
	.p2align	4, 0x90
	.type	MPI_Send_init,@function
MPI_Send_init:                          # @MPI_Send_init
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$5, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Send_init
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_6, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end5:
	.size	MPI_Send_init, .Lfunc_end5-MPI_Send_init
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Ibsend              # -- Begin function MPI_Ibsend
	.p2align	4, 0x90
	.type	MPI_Ibsend,@function
MPI_Ibsend:                             # @MPI_Ibsend
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$6, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Ibsend
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_7, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end6:
	.size	MPI_Ibsend, .Lfunc_end6-MPI_Ibsend
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Irecv               # -- Begin function MPI_Irecv
	.p2align	4, 0x90
	.type	MPI_Irecv,@function
MPI_Irecv:                              # @MPI_Irecv
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$7, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Irecv
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_8, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end7:
	.size	MPI_Irecv, .Lfunc_end7-MPI_Irecv
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Irsend              # -- Begin function MPI_Irsend
	.p2align	4, 0x90
	.type	MPI_Irsend,@function
MPI_Irsend:                             # @MPI_Irsend
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$8, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Irsend
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_9, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end8:
	.size	MPI_Irsend, .Lfunc_end8-MPI_Irsend
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Isend               # -- Begin function MPI_Isend
	.p2align	4, 0x90
	.type	MPI_Isend,@function
MPI_Isend:                              # @MPI_Isend
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$9, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Isend
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_10, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end9:
	.size	MPI_Isend, .Lfunc_end9-MPI_Isend
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Issend              # -- Begin function MPI_Issend
	.p2align	4, 0x90
	.type	MPI_Issend,@function
MPI_Issend:                             # @MPI_Issend
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$10, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Issend
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_11, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end10:
	.size	MPI_Issend, .Lfunc_end10-MPI_Issend
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Recv                # -- Begin function MPI_Recv
	.p2align	4, 0x90
	.type	MPI_Recv,@function
MPI_Recv:                               # @MPI_Recv
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$136, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$11, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Recv
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_12, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$136, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end11:
	.size	MPI_Recv, .Lfunc_end11-MPI_Recv
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Rsend               # -- Begin function MPI_Rsend
	.p2align	4, 0x90
	.type	MPI_Rsend,@function
MPI_Rsend:                              # @MPI_Rsend
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	$12, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	callq	PMPI_Rsend
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_13, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end12:
	.size	MPI_Rsend, .Lfunc_end12-MPI_Rsend
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Rsend_init          # -- Begin function MPI_Rsend_init
	.p2align	4, 0x90
	.type	MPI_Rsend_init,@function
MPI_Rsend_init:                         # @MPI_Rsend_init
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$13, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Rsend_init
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_14, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end13:
	.size	MPI_Rsend_init, .Lfunc_end13-MPI_Rsend_init
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Send                # -- Begin function MPI_Send
	.p2align	4, 0x90
	.type	MPI_Send,@function
MPI_Send:                               # @MPI_Send
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	$14, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	callq	PMPI_Send
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_15, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end14:
	.size	MPI_Send, .Lfunc_end14-MPI_Send
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Sendrecv            # -- Begin function MPI_Sendrecv
	.p2align	4, 0x90
	.type	MPI_Sendrecv,@function
MPI_Sendrecv:                           # @MPI_Sendrecv
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$152, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -72(%rbp)          # 8-byte Spill
	movl	%r8d, %r12d
	movl	%ecx, %r13d
	movl	%edx, %ebx
	movl	%esi, %r14d
	movq	%rdi, %r15
	movq	56(%rbp), %rax
	movl	48(%rbp), %eax
	movl	40(%rbp), %eax
	movl	32(%rbp), %eax
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movl	$15, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r15, -96(%rbp)
	movl	%r14d, -60(%rbp)
	movl	%ebx, -56(%rbp)
	movl	%r13d, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	-72(%rbp), %rax         # 8-byte Reload
	movq	%rax, -88(%rbp)
	movq	-96(%rbp), %rdi
	movl	-60(%rbp), %esi
	movl	-56(%rbp), %edx
	movl	-52(%rbp), %ecx
	movl	-48(%rbp), %r8d
	movq	-88(%rbp), %r9
	movl	16(%rbp), %eax
	movl	24(%rbp), %ebx
	movl	32(%rbp), %r10d
	movl	40(%rbp), %r11d
	movl	48(%rbp), %r14d
	movq	56(%rbp), %r15
	movl	%eax, (%rsp)
	movl	%ebx, 8(%rsp)
	movl	%r10d, 16(%rsp)
	movl	%r11d, 24(%rsp)
	movl	%r14d, 32(%rsp)
	movq	%r15, 40(%rsp)
	callq	PMPI_Sendrecv
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_16, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$152, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end15:
	.size	MPI_Sendrecv, .Lfunc_end15-MPI_Sendrecv
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Sendrecv_replace    # -- Begin function MPI_Sendrecv_replace
	.p2align	4, 0x90
	.type	MPI_Sendrecv_replace,@function
MPI_Sendrecv_replace:                   # @MPI_Sendrecv_replace
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$120, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	32(%rbp), %rax
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movl	$16, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	24(%rbp), %ebx
	movq	32(%rbp), %r10
	movl	%eax, (%rsp)
	movl	%ebx, 8(%rsp)
	movq	%r10, 16(%rsp)
	callq	PMPI_Sendrecv_replace
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_17, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$120, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end16:
	.size	MPI_Sendrecv_replace, .Lfunc_end16-MPI_Sendrecv_replace
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Ssend               # -- Begin function MPI_Ssend
	.p2align	4, 0x90
	.type	MPI_Ssend,@function
MPI_Ssend:                              # @MPI_Ssend
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	$17, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	callq	PMPI_Ssend
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_18, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end17:
	.size	MPI_Ssend, .Lfunc_end17-MPI_Ssend
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Ssend_init          # -- Begin function MPI_Ssend_init
	.p2align	4, 0x90
	.type	MPI_Ssend_init,@function
MPI_Ssend_init:                         # @MPI_Ssend_init
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movq	16(%rbp), %rax
	movl	$18, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -68(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-68(%rbp), %esi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movq	16(%rbp), %rax
	movq	%rax, (%rsp)
	callq	PMPI_Ssend_init
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_19, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end18:
	.size	MPI_Ssend_init, .Lfunc_end18-MPI_Ssend_init
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Test                # -- Begin function MPI_Test
	.p2align	4, 0x90
	.type	MPI_Test,@function
MPI_Test:                               # @MPI_Test
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$80, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movq	%rsi, %r15
	movq	%rdi, %rbx
	movl	$19, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movq	%rbx, -64(%rbp)
	movq	%r15, -56(%rbp)
	movq	%r14, -48(%rbp)
	movq	-64(%rbp), %rdi
	movq	-56(%rbp), %rsi
	movq	-48(%rbp), %rdx
	callq	PMPI_Test
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_20, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$80, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end19:
	.size	MPI_Test, .Lfunc_end19-MPI_Test
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Testall             # -- Begin function MPI_Testall
	.p2align	4, 0x90
	.type	MPI_Testall,@function
MPI_Testall:                            # @MPI_Testall
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movq	%rsi, %r12
	movl	%edi, %ebx
	movl	$20, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -48(%rbp)
	movq	%r12, -72(%rbp)
	movq	%r15, -64(%rbp)
	movq	%r14, -56(%rbp)
	movl	-48(%rbp), %edi
	movq	-72(%rbp), %rsi
	movq	-64(%rbp), %rdx
	movq	-56(%rbp), %rcx
	callq	PMPI_Testall
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_21, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end20:
	.size	MPI_Testall, .Lfunc_end20-MPI_Testall
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Testany             # -- Begin function MPI_Testany
	.p2align	4, 0x90
	.type	MPI_Testany,@function
MPI_Testany:                            # @MPI_Testany
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movq	%rdx, %r12
	movq	%rsi, %r13
	movl	%edi, %ebx
	movl	$21, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -56(%rbp)         # 8-byte Spill
	movl	%ebx, -48(%rbp)
	movq	%r13, -88(%rbp)
	movq	%r12, -80(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-48(%rbp), %edi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movq	-72(%rbp), %rcx
	movq	-64(%rbp), %r8
	callq	PMPI_Testany
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_22, %rdi
	movq	-56(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end21:
	.size	MPI_Testany, .Lfunc_end21-MPI_Testany
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Test_cancelled      # -- Begin function MPI_Test_cancelled
	.p2align	4, 0x90
	.type	MPI_Test_cancelled,@function
MPI_Test_cancelled:                     # @MPI_Test_cancelled
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movq	%rdi, %rbx
	movl	$22, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -48(%rbp)
	movq	%r14, -40(%rbp)
	movq	-48(%rbp), %rdi
	movq	-40(%rbp), %rsi
	callq	PMPI_Test_cancelled
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_23, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end22:
	.size	MPI_Test_cancelled, .Lfunc_end22-MPI_Test_cancelled
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Testsome            # -- Begin function MPI_Testsome
	.p2align	4, 0x90
	.type	MPI_Testsome,@function
MPI_Testsome:                           # @MPI_Testsome
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movq	%rdx, %r12
	movq	%rsi, %r13
	movl	%edi, %ebx
	movl	$23, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -56(%rbp)         # 8-byte Spill
	movl	%ebx, -48(%rbp)
	movq	%r13, -88(%rbp)
	movq	%r12, -80(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-48(%rbp), %edi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movq	-72(%rbp), %rcx
	movq	-64(%rbp), %r8
	callq	PMPI_Testsome
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_24, %rdi
	movq	-56(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end23:
	.size	MPI_Testsome, .Lfunc_end23-MPI_Testsome
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Wait                # -- Begin function MPI_Wait
	.p2align	4, 0x90
	.type	MPI_Wait,@function
MPI_Wait:                               # @MPI_Wait
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movq	%rdi, %rbx
	movl	$24, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -48(%rbp)
	movq	%r14, -40(%rbp)
	movq	-48(%rbp), %rdi
	movq	-40(%rbp), %rsi
	callq	PMPI_Wait
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_25, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end24:
	.size	MPI_Wait, .Lfunc_end24-MPI_Wait
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Waitall             # -- Begin function MPI_Waitall
	.p2align	4, 0x90
	.type	MPI_Waitall,@function
MPI_Waitall:                            # @MPI_Waitall
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movq	%rsi, %r15
	movl	%edi, %ebx
	movl	$25, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -40(%rbp)
	movq	%r15, -56(%rbp)
	movq	%r14, -48(%rbp)
	movl	-40(%rbp), %edi
	movq	-56(%rbp), %rsi
	movq	-48(%rbp), %rdx
	callq	PMPI_Waitall
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_26, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end25:
	.size	MPI_Waitall, .Lfunc_end25-MPI_Waitall
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Waitany             # -- Begin function MPI_Waitany
	.p2align	4, 0x90
	.type	MPI_Waitany,@function
MPI_Waitany:                            # @MPI_Waitany
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movq	%rsi, %r12
	movl	%edi, %ebx
	movl	$26, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -48(%rbp)
	movq	%r12, -72(%rbp)
	movq	%r15, -64(%rbp)
	movq	%r14, -56(%rbp)
	movl	-48(%rbp), %edi
	movq	-72(%rbp), %rsi
	movq	-64(%rbp), %rdx
	movq	-56(%rbp), %rcx
	callq	PMPI_Waitany
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_27, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end26:
	.size	MPI_Waitany, .Lfunc_end26-MPI_Waitany
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Waitsome            # -- Begin function MPI_Waitsome
	.p2align	4, 0x90
	.type	MPI_Waitsome,@function
MPI_Waitsome:                           # @MPI_Waitsome
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movq	%rdx, %r12
	movq	%rsi, %r13
	movl	%edi, %ebx
	movl	$27, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -56(%rbp)         # 8-byte Spill
	movl	%ebx, -48(%rbp)
	movq	%r13, -88(%rbp)
	movq	%r12, -80(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-48(%rbp), %edi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movq	-72(%rbp), %rcx
	movq	-64(%rbp), %r8
	callq	PMPI_Waitsome
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_28, %rdi
	movq	-56(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end27:
	.size	MPI_Waitsome, .Lfunc_end27-MPI_Waitsome
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cancel              # -- Begin function MPI_Cancel
	.p2align	4, 0x90
	.type	MPI_Cancel,@function
MPI_Cancel:                             # @MPI_Cancel
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$28, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Cancel
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_29, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end28:
	.size	MPI_Cancel, .Lfunc_end28-MPI_Cancel
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Request_free        # -- Begin function MPI_Request_free
	.p2align	4, 0x90
	.type	MPI_Request_free,@function
MPI_Request_free:                       # @MPI_Request_free
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$29, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Request_free
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_30, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end29:
	.size	MPI_Request_free, .Lfunc_end29-MPI_Request_free
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Start               # -- Begin function MPI_Start
	.p2align	4, 0x90
	.type	MPI_Start,@function
MPI_Start:                              # @MPI_Start
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$30, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Start
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_31, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end30:
	.size	MPI_Start, .Lfunc_end30-MPI_Start
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Startall            # -- Begin function MPI_Startall
	.p2align	4, 0x90
	.type	MPI_Startall,@function
MPI_Startall:                           # @MPI_Startall
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$31, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Startall
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_32, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end31:
	.size	MPI_Startall, .Lfunc_end31-MPI_Startall
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Iprobe              # -- Begin function MPI_Iprobe
	.p2align	4, 0x90
	.type	MPI_Iprobe,@function
MPI_Iprobe:                             # @MPI_Iprobe
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movl	%edx, %r12d
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$32, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -56(%rbp)
	movl	%r13d, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -80(%rbp)
	movq	%r14, -72(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-80(%rbp), %rcx
	movq	-72(%rbp), %r8
	callq	PMPI_Iprobe
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_33, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end32:
	.size	MPI_Iprobe, .Lfunc_end32-MPI_Iprobe
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Probe               # -- Begin function MPI_Probe
	.p2align	4, 0x90
	.type	MPI_Probe,@function
MPI_Probe:                              # @MPI_Probe
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movl	%edx, %r15d
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$33, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -56(%rbp)
	movl	%r12d, -52(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -64(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-64(%rbp), %rcx
	callq	PMPI_Probe
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_34, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end33:
	.size	MPI_Probe, .Lfunc_end33-MPI_Probe
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Allgather           # -- Begin function MPI_Allgather
	.p2align	4, 0x90
	.type	MPI_Allgather,@function
MPI_Allgather:                          # @MPI_Allgather
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	16(%rbp), %eax
	movl	$34, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -64(%rbp)
	movl	%r13d, -60(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-64(%rbp), %esi
	movl	-60(%rbp), %edx
	movq	-80(%rbp), %rcx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	%eax, (%rsp)
	callq	PMPI_Allgather
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_35, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end34:
	.size	MPI_Allgather, .Lfunc_end34-MPI_Allgather
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Allgatherv          # -- Begin function MPI_Allgatherv
	.p2align	4, 0x90
	.type	MPI_Allgatherv,@function
MPI_Allgatherv:                         # @MPI_Allgatherv
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$120, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -64(%rbp)          # 8-byte Spill
	movq	%r8, %r15
	movq	%rcx, %r12
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movl	$35, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -104(%rbp)
	movl	%ebx, -52(%rbp)
	movl	%r13d, -48(%rbp)
	movq	%r12, -96(%rbp)
	movq	%r15, -88(%rbp)
	movq	-64(%rbp), %rax         # 8-byte Reload
	movq	%rax, -80(%rbp)
	movq	-104(%rbp), %rdi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-96(%rbp), %rcx
	movq	-88(%rbp), %r8
	movq	-80(%rbp), %r9
	movl	16(%rbp), %eax
	movl	24(%rbp), %ebx
	movl	%eax, (%rsp)
	movl	%ebx, 8(%rsp)
	callq	PMPI_Allgatherv
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_36, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$120, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end35:
	.size	MPI_Allgatherv, .Lfunc_end35-MPI_Allgatherv
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Allreduce           # -- Begin function MPI_Allreduce
	.p2align	4, 0x90
	.type	MPI_Allreduce,@function
MPI_Allreduce:                          # @MPI_Allreduce
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movq	%rsi, %rbx
	movq	%rdi, %r14
	movl	$36, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movq	%rbx, -80(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movq	-80(%rbp), %rsi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	callq	PMPI_Allreduce
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_37, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end36:
	.size	MPI_Allreduce, .Lfunc_end36-MPI_Allreduce
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Alltoall            # -- Begin function MPI_Alltoall
	.p2align	4, 0x90
	.type	MPI_Alltoall,@function
MPI_Alltoall:                           # @MPI_Alltoall
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	16(%rbp), %eax
	movl	$37, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -64(%rbp)
	movl	%r13d, -60(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-64(%rbp), %esi
	movl	-60(%rbp), %edx
	movq	-80(%rbp), %rcx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	%eax, (%rsp)
	callq	PMPI_Alltoall
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_38, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end37:
	.size	MPI_Alltoall, .Lfunc_end37-MPI_Alltoall
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Alltoallv           # -- Begin function MPI_Alltoallv
	.p2align	4, 0x90
	.type	MPI_Alltoallv,@function
MPI_Alltoallv:                          # @MPI_Alltoallv
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$136, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -56(%rbp)          # 8-byte Spill
	movq	%r8, %r15
	movl	%ecx, %r12d
	movq	%rdx, %r13
	movq	%rsi, %rbx
	movq	%rdi, %r14
	movl	32(%rbp), %eax
	movl	24(%rbp), %eax
	movq	16(%rbp), %rax
	movl	$38, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movq	%r14, -104(%rbp)
	movq	%rbx, -96(%rbp)
	movq	%r13, -88(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -80(%rbp)
	movq	-56(%rbp), %rax         # 8-byte Reload
	movq	%rax, -72(%rbp)
	movq	-104(%rbp), %rdi
	movq	-96(%rbp), %rsi
	movq	-88(%rbp), %rdx
	movl	-48(%rbp), %ecx
	movq	-80(%rbp), %r8
	movq	-72(%rbp), %r9
	movq	16(%rbp), %rax
	movl	24(%rbp), %ebx
	movl	32(%rbp), %r10d
	movq	%rax, (%rsp)
	movl	%ebx, 8(%rsp)
	movl	%r10d, 16(%rsp)
	callq	PMPI_Alltoallv
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_39, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$136, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end38:
	.size	MPI_Alltoallv, .Lfunc_end38-MPI_Alltoallv
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Barrier             # -- Begin function MPI_Barrier
	.p2align	4, 0x90
	.type	MPI_Barrier,@function
MPI_Barrier:                            # @MPI_Barrier
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$48, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movl	%edi, %ebx
	movl	$39, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movl	%ebx, -24(%rbp)
	movl	-24(%rbp), %edi
	callq	PMPI_Barrier
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_40, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$48, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end39:
	.size	MPI_Barrier, .Lfunc_end39-MPI_Barrier
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Bcast               # -- Begin function MPI_Bcast
	.p2align	4, 0x90
	.type	MPI_Bcast,@function
MPI_Bcast:                              # @MPI_Bcast
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r8d, %r14d
	movl	%ecx, %r15d
	movl	%edx, %r12d
	movl	%esi, %r13d
	movq	%rdi, %rbx
	movl	$40, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%rbx, -80(%rbp)
	movl	%r13d, -60(%rbp)
	movl	%r12d, -56(%rbp)
	movl	%r15d, -52(%rbp)
	movl	%r14d, -48(%rbp)
	movq	-80(%rbp), %rdi
	movl	-60(%rbp), %esi
	movl	-56(%rbp), %edx
	movl	-52(%rbp), %ecx
	movl	-48(%rbp), %r8d
	callq	PMPI_Bcast
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_41, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end40:
	.size	MPI_Bcast, .Lfunc_end40-MPI_Bcast
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Gather              # -- Begin function MPI_Gather
	.p2align	4, 0x90
	.type	MPI_Gather,@function
MPI_Gather:                             # @MPI_Gather
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movl	$41, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -64(%rbp)
	movl	%r13d, -60(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-64(%rbp), %esi
	movl	-60(%rbp), %edx
	movq	-80(%rbp), %rcx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	24(%rbp), %ebx
	movl	%eax, (%rsp)
	movl	%ebx, 8(%rsp)
	callq	PMPI_Gather
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_42, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end41:
	.size	MPI_Gather, .Lfunc_end41-MPI_Gather
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Gatherv             # -- Begin function MPI_Gatherv
	.p2align	4, 0x90
	.type	MPI_Gatherv,@function
MPI_Gatherv:                            # @MPI_Gatherv
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$136, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -64(%rbp)          # 8-byte Spill
	movq	%r8, %r15
	movq	%rcx, %r12
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	32(%rbp), %eax
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movl	$42, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -104(%rbp)
	movl	%ebx, -52(%rbp)
	movl	%r13d, -48(%rbp)
	movq	%r12, -96(%rbp)
	movq	%r15, -88(%rbp)
	movq	-64(%rbp), %rax         # 8-byte Reload
	movq	%rax, -80(%rbp)
	movq	-104(%rbp), %rdi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-96(%rbp), %rcx
	movq	-88(%rbp), %r8
	movq	-80(%rbp), %r9
	movl	16(%rbp), %eax
	movl	24(%rbp), %ebx
	movl	32(%rbp), %r10d
	movl	%eax, (%rsp)
	movl	%ebx, 8(%rsp)
	movl	%r10d, 16(%rsp)
	callq	PMPI_Gatherv
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_43, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$136, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end42:
	.size	MPI_Gatherv, .Lfunc_end42-MPI_Gatherv
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Reduce_scatter      # -- Begin function MPI_Reduce_scatter
	.p2align	4, 0x90
	.type	MPI_Reduce_scatter,@function
MPI_Reduce_scatter:                     # @MPI_Reduce_scatter
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movq	%rdx, %r13
	movq	%rsi, %rbx
	movq	%rdi, %r14
	movl	$43, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -96(%rbp)
	movq	%rbx, -88(%rbp)
	movq	%r13, -80(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-96(%rbp), %rdi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	callq	PMPI_Reduce_scatter
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_44, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end43:
	.size	MPI_Reduce_scatter, .Lfunc_end43-MPI_Reduce_scatter
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Reduce              # -- Begin function MPI_Reduce
	.p2align	4, 0x90
	.type	MPI_Reduce,@function
MPI_Reduce:                             # @MPI_Reduce
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movq	%rsi, %rbx
	movq	%rdi, %r14
	movl	16(%rbp), %eax
	movl	$44, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movq	%rbx, -80(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movq	-80(%rbp), %rsi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	%eax, (%rsp)
	callq	PMPI_Reduce
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_45, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end44:
	.size	MPI_Reduce, .Lfunc_end44-MPI_Reduce
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Scan                # -- Begin function MPI_Scan
	.p2align	4, 0x90
	.type	MPI_Scan,@function
MPI_Scan:                               # @MPI_Scan
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movq	%rsi, %rbx
	movq	%rdi, %r14
	movl	$45, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movq	%rbx, -80(%rbp)
	movl	%r13d, -64(%rbp)
	movl	%r12d, -60(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movq	-80(%rbp), %rsi
	movl	-64(%rbp), %edx
	movl	-60(%rbp), %ecx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	callq	PMPI_Scan
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_46, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end45:
	.size	MPI_Scan, .Lfunc_end45-MPI_Scan
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Scatter             # -- Begin function MPI_Scatter
	.p2align	4, 0x90
	.type	MPI_Scatter,@function
MPI_Scatter:                            # @MPI_Scatter
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movl	$46, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -88(%rbp)
	movl	%ebx, -64(%rbp)
	movl	%r13d, -60(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-88(%rbp), %rdi
	movl	-64(%rbp), %esi
	movl	-60(%rbp), %edx
	movq	-80(%rbp), %rcx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	24(%rbp), %ebx
	movl	%eax, (%rsp)
	movl	%ebx, 8(%rsp)
	callq	PMPI_Scatter
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_47, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end46:
	.size	MPI_Scatter, .Lfunc_end46-MPI_Scatter
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Scatterv            # -- Begin function MPI_Scatterv
	.p2align	4, 0x90
	.type	MPI_Scatterv,@function
MPI_Scatterv:                           # @MPI_Scatterv
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$120, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movq	%r8, %r15
	movl	%ecx, %r12d
	movq	%rdx, %r13
	movq	%rsi, %rbx
	movq	%rdi, %r14
	movl	32(%rbp), %eax
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movl	$47, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movq	%r14, -96(%rbp)
	movq	%rbx, -88(%rbp)
	movq	%r13, -80(%rbp)
	movl	%r12d, -56(%rbp)
	movq	%r15, -72(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-96(%rbp), %rdi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movl	-56(%rbp), %ecx
	movq	-72(%rbp), %r8
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	24(%rbp), %ebx
	movl	32(%rbp), %r10d
	movl	%eax, (%rsp)
	movl	%ebx, 8(%rsp)
	movl	%r10d, 16(%rsp)
	callq	PMPI_Scatterv
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_48, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$120, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end47:
	.size	MPI_Scatterv, .Lfunc_end47-MPI_Scatterv
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_compare        # -- Begin function MPI_Comm_compare
	.p2align	4, 0x90
	.type	MPI_Comm_compare,@function
MPI_Comm_compare:                       # @MPI_Comm_compare
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$48, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Comm_compare
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_49, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end48:
	.size	MPI_Comm_compare, .Lfunc_end48-MPI_Comm_compare
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_create         # -- Begin function MPI_Comm_create
	.p2align	4, 0x90
	.type	MPI_Comm_create,@function
MPI_Comm_create:                        # @MPI_Comm_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$49, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Comm_create
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_50, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end49:
	.size	MPI_Comm_create, .Lfunc_end49-MPI_Comm_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_dup            # -- Begin function MPI_Comm_dup
	.p2align	4, 0x90
	.type	MPI_Comm_dup,@function
MPI_Comm_dup:                           # @MPI_Comm_dup
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$50, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Comm_dup
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_51, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end50:
	.size	MPI_Comm_dup, .Lfunc_end50-MPI_Comm_dup
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_free           # -- Begin function MPI_Comm_free
	.p2align	4, 0x90
	.type	MPI_Comm_free,@function
MPI_Comm_free:                          # @MPI_Comm_free
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$51, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Comm_free
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_52, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end51:
	.size	MPI_Comm_free, .Lfunc_end51-MPI_Comm_free
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_group          # -- Begin function MPI_Comm_group
	.p2align	4, 0x90
	.type	MPI_Comm_group,@function
MPI_Comm_group:                         # @MPI_Comm_group
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$52, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Comm_group
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_53, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end52:
	.size	MPI_Comm_group, .Lfunc_end52-MPI_Comm_group
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_rank           # -- Begin function MPI_Comm_rank
	.p2align	4, 0x90
	.type	MPI_Comm_rank,@function
MPI_Comm_rank:                          # @MPI_Comm_rank
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$53, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Comm_rank
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_54, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end53:
	.size	MPI_Comm_rank, .Lfunc_end53-MPI_Comm_rank
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_remote_group   # -- Begin function MPI_Comm_remote_group
	.p2align	4, 0x90
	.type	MPI_Comm_remote_group,@function
MPI_Comm_remote_group:                  # @MPI_Comm_remote_group
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$54, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Comm_remote_group
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_55, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end54:
	.size	MPI_Comm_remote_group, .Lfunc_end54-MPI_Comm_remote_group
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_remote_size    # -- Begin function MPI_Comm_remote_size
	.p2align	4, 0x90
	.type	MPI_Comm_remote_size,@function
MPI_Comm_remote_size:                   # @MPI_Comm_remote_size
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$55, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Comm_remote_size
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_56, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end55:
	.size	MPI_Comm_remote_size, .Lfunc_end55-MPI_Comm_remote_size
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_size           # -- Begin function MPI_Comm_size
	.p2align	4, 0x90
	.type	MPI_Comm_size,@function
MPI_Comm_size:                          # @MPI_Comm_size
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$56, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Comm_size
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_57, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end56:
	.size	MPI_Comm_size, .Lfunc_end56-MPI_Comm_size
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_split          # -- Begin function MPI_Comm_split
	.p2align	4, 0x90
	.type	MPI_Comm_split,@function
MPI_Comm_split:                         # @MPI_Comm_split
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movl	%edx, %r15d
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$57, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -56(%rbp)
	movl	%r12d, -52(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -64(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-64(%rbp), %rcx
	callq	PMPI_Comm_split
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_58, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end57:
	.size	MPI_Comm_split, .Lfunc_end57-MPI_Comm_split
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Comm_test_inter     # -- Begin function MPI_Comm_test_inter
	.p2align	4, 0x90
	.type	MPI_Comm_test_inter,@function
MPI_Comm_test_inter:                    # @MPI_Comm_test_inter
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$58, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Comm_test_inter
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_59, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end58:
	.size	MPI_Comm_test_inter, .Lfunc_end58-MPI_Comm_test_inter
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_compare       # -- Begin function MPI_Group_compare
	.p2align	4, 0x90
	.type	MPI_Group_compare,@function
MPI_Group_compare:                      # @MPI_Group_compare
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$59, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Group_compare
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_60, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end59:
	.size	MPI_Group_compare, .Lfunc_end59-MPI_Group_compare
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_difference    # -- Begin function MPI_Group_difference
	.p2align	4, 0x90
	.type	MPI_Group_difference,@function
MPI_Group_difference:                   # @MPI_Group_difference
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$60, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Group_difference
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_61, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end60:
	.size	MPI_Group_difference, .Lfunc_end60-MPI_Group_difference
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_excl          # -- Begin function MPI_Group_excl
	.p2align	4, 0x90
	.type	MPI_Group_excl,@function
MPI_Group_excl:                         # @MPI_Group_excl
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$61, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-72(%rbp), %rdx
	movq	-64(%rbp), %rcx
	callq	PMPI_Group_excl
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_62, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end61:
	.size	MPI_Group_excl, .Lfunc_end61-MPI_Group_excl
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_free          # -- Begin function MPI_Group_free
	.p2align	4, 0x90
	.type	MPI_Group_free,@function
MPI_Group_free:                         # @MPI_Group_free
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$62, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Group_free
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_63, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end62:
	.size	MPI_Group_free, .Lfunc_end62-MPI_Group_free
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_incl          # -- Begin function MPI_Group_incl
	.p2align	4, 0x90
	.type	MPI_Group_incl,@function
MPI_Group_incl:                         # @MPI_Group_incl
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$63, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-72(%rbp), %rdx
	movq	-64(%rbp), %rcx
	callq	PMPI_Group_incl
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_64, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end63:
	.size	MPI_Group_incl, .Lfunc_end63-MPI_Group_incl
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_intersection  # -- Begin function MPI_Group_intersection
	.p2align	4, 0x90
	.type	MPI_Group_intersection,@function
MPI_Group_intersection:                 # @MPI_Group_intersection
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$64, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Group_intersection
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_65, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end64:
	.size	MPI_Group_intersection, .Lfunc_end64-MPI_Group_intersection
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_rank          # -- Begin function MPI_Group_rank
	.p2align	4, 0x90
	.type	MPI_Group_rank,@function
MPI_Group_rank:                         # @MPI_Group_rank
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$65, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Group_rank
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_66, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end65:
	.size	MPI_Group_rank, .Lfunc_end65-MPI_Group_rank
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_range_excl    # -- Begin function MPI_Group_range_excl
	.p2align	4, 0x90
	.type	MPI_Group_range_excl,@function
MPI_Group_range_excl:                   # @MPI_Group_range_excl
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$66, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-72(%rbp), %rdx
	movq	-64(%rbp), %rcx
	callq	PMPI_Group_range_excl
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_67, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end66:
	.size	MPI_Group_range_excl, .Lfunc_end66-MPI_Group_range_excl
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_range_incl    # -- Begin function MPI_Group_range_incl
	.p2align	4, 0x90
	.type	MPI_Group_range_incl,@function
MPI_Group_range_incl:                   # @MPI_Group_range_incl
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$67, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-72(%rbp), %rdx
	movq	-64(%rbp), %rcx
	callq	PMPI_Group_range_incl
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_68, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end67:
	.size	MPI_Group_range_incl, .Lfunc_end67-MPI_Group_range_incl
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_size          # -- Begin function MPI_Group_size
	.p2align	4, 0x90
	.type	MPI_Group_size,@function
MPI_Group_size:                         # @MPI_Group_size
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$68, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Group_size
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_69, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end68:
	.size	MPI_Group_size, .Lfunc_end68-MPI_Group_size
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_translate_ranks # -- Begin function MPI_Group_translate_ranks
	.p2align	4, 0x90
	.type	MPI_Group_translate_ranks,@function
MPI_Group_translate_ranks:              # @MPI_Group_translate_ranks
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movl	%ecx, %r15d
	movq	%rdx, %r12
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$69, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -56(%rbp)
	movl	%r13d, -52(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -72(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movq	-80(%rbp), %rdx
	movl	-48(%rbp), %ecx
	movq	-72(%rbp), %r8
	callq	PMPI_Group_translate_ranks
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_70, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end69:
	.size	MPI_Group_translate_ranks, .Lfunc_end69-MPI_Group_translate_ranks
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Group_union         # -- Begin function MPI_Group_union
	.p2align	4, 0x90
	.type	MPI_Group_union,@function
MPI_Group_union:                        # @MPI_Group_union
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$70, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Group_union
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_71, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end70:
	.size	MPI_Group_union, .Lfunc_end70-MPI_Group_union
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Intercomm_create    # -- Begin function MPI_Intercomm_create
	.p2align	4, 0x90
	.type	MPI_Intercomm_create,@function
MPI_Intercomm_create:                   # @MPI_Intercomm_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -72(%rbp)          # 8-byte Spill
	movl	%r8d, %r15d
	movl	%ecx, %r12d
	movl	%edx, %r13d
	movl	%esi, %ebx
	movl	%edi, %r14d
	movl	$71, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -80(%rbp)         # 8-byte Spill
	movl	%r14d, -64(%rbp)
	movl	%ebx, -60(%rbp)
	movl	%r13d, -56(%rbp)
	movl	%r12d, -52(%rbp)
	movl	%r15d, -48(%rbp)
	movq	-72(%rbp), %rax         # 8-byte Reload
	movq	%rax, -88(%rbp)
	movl	-64(%rbp), %edi
	movl	-60(%rbp), %esi
	movl	-56(%rbp), %edx
	movl	-52(%rbp), %ecx
	movl	-48(%rbp), %r8d
	movq	-88(%rbp), %r9
	callq	PMPI_Intercomm_create
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_72, %rdi
	movq	-80(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end71:
	.size	MPI_Intercomm_create, .Lfunc_end71-MPI_Intercomm_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Intercomm_merge     # -- Begin function MPI_Intercomm_merge
	.p2align	4, 0x90
	.type	MPI_Intercomm_merge,@function
MPI_Intercomm_merge:                    # @MPI_Intercomm_merge
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$72, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Intercomm_merge
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_73, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end72:
	.size	MPI_Intercomm_merge, .Lfunc_end72-MPI_Intercomm_merge
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Keyval_create       # -- Begin function MPI_Keyval_create
	.p2align	4, 0x90
	.type	MPI_Keyval_create,@function
MPI_Keyval_create:                      # @MPI_Keyval_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movq	%rsi, %r12
	movq	%rdi, %rbx
	movl	$73, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movq	%rbx, -80(%rbp)
	movq	%r12, -72(%rbp)
	movq	%r15, -64(%rbp)
	movq	%r14, -56(%rbp)
	movq	-80(%rbp), %rdi
	movq	-72(%rbp), %rsi
	movq	-64(%rbp), %rdx
	movq	-56(%rbp), %rcx
	callq	PMPI_Keyval_create
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_74, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end73:
	.size	MPI_Keyval_create, .Lfunc_end73-MPI_Keyval_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Keyval_free         # -- Begin function MPI_Keyval_free
	.p2align	4, 0x90
	.type	MPI_Keyval_free,@function
MPI_Keyval_free:                        # @MPI_Keyval_free
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$74, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Keyval_free
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_75, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end74:
	.size	MPI_Keyval_free, .Lfunc_end74-MPI_Keyval_free
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cart_coords         # -- Begin function MPI_Cart_coords
	.p2align	4, 0x90
	.type	MPI_Cart_coords,@function
MPI_Cart_coords:                        # @MPI_Cart_coords
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movl	%edx, %r15d
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$75, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -56(%rbp)
	movl	%r12d, -52(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -64(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-64(%rbp), %rcx
	callq	PMPI_Cart_coords
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_76, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end75:
	.size	MPI_Cart_coords, .Lfunc_end75-MPI_Cart_coords
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cart_create         # -- Begin function MPI_Cart_create
	.p2align	4, 0x90
	.type	MPI_Cart_create,@function
MPI_Cart_create:                        # @MPI_Cart_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -64(%rbp)          # 8-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movq	%rdx, %r13
	movl	%esi, %ebx
	movl	%edi, %r14d
	movl	$76, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movl	%r14d, -56(%rbp)
	movl	%ebx, -52(%rbp)
	movq	%r13, -96(%rbp)
	movq	%r12, -88(%rbp)
	movl	%r15d, -48(%rbp)
	movq	-64(%rbp), %rax         # 8-byte Reload
	movq	%rax, -80(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movq	-96(%rbp), %rdx
	movq	-88(%rbp), %rcx
	movl	-48(%rbp), %r8d
	movq	-80(%rbp), %r9
	callq	PMPI_Cart_create
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_77, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end76:
	.size	MPI_Cart_create, .Lfunc_end76-MPI_Cart_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cart_get            # -- Begin function MPI_Cart_get
	.p2align	4, 0x90
	.type	MPI_Cart_get,@function
MPI_Cart_get:                           # @MPI_Cart_get
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movq	%rdx, %r12
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$77, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -52(%rbp)
	movl	%r13d, -48(%rbp)
	movq	%r12, -88(%rbp)
	movq	%r15, -80(%rbp)
	movq	%r14, -72(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-88(%rbp), %rdx
	movq	-80(%rbp), %rcx
	movq	-72(%rbp), %r8
	callq	PMPI_Cart_get
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_78, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end77:
	.size	MPI_Cart_get, .Lfunc_end77-MPI_Cart_get
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cart_map            # -- Begin function MPI_Cart_map
	.p2align	4, 0x90
	.type	MPI_Cart_map,@function
MPI_Cart_map:                           # @MPI_Cart_map
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movq	%rdx, %r12
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$78, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -52(%rbp)
	movl	%r13d, -48(%rbp)
	movq	%r12, -88(%rbp)
	movq	%r15, -80(%rbp)
	movq	%r14, -72(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-88(%rbp), %rdx
	movq	-80(%rbp), %rcx
	movq	-72(%rbp), %r8
	callq	PMPI_Cart_map
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_79, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end78:
	.size	MPI_Cart_map, .Lfunc_end78-MPI_Cart_map
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cart_rank           # -- Begin function MPI_Cart_rank
	.p2align	4, 0x90
	.type	MPI_Cart_rank,@function
MPI_Cart_rank:                          # @MPI_Cart_rank
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movq	%rsi, %r15
	movl	%edi, %ebx
	movl	$79, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -40(%rbp)
	movq	%r15, -56(%rbp)
	movq	%r14, -48(%rbp)
	movl	-40(%rbp), %edi
	movq	-56(%rbp), %rsi
	movq	-48(%rbp), %rdx
	callq	PMPI_Cart_rank
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_80, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end79:
	.size	MPI_Cart_rank, .Lfunc_end79-MPI_Cart_rank
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cart_shift          # -- Begin function MPI_Cart_shift
	.p2align	4, 0x90
	.type	MPI_Cart_shift,@function
MPI_Cart_shift:                         # @MPI_Cart_shift
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movl	%edx, %r12d
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$80, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -56(%rbp)
	movl	%r13d, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -80(%rbp)
	movq	%r14, -72(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-80(%rbp), %rcx
	movq	-72(%rbp), %r8
	callq	PMPI_Cart_shift
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_81, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end80:
	.size	MPI_Cart_shift, .Lfunc_end80-MPI_Cart_shift
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cart_sub            # -- Begin function MPI_Cart_sub
	.p2align	4, 0x90
	.type	MPI_Cart_sub,@function
MPI_Cart_sub:                           # @MPI_Cart_sub
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movq	%rsi, %r15
	movl	%edi, %ebx
	movl	$81, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -40(%rbp)
	movq	%r15, -56(%rbp)
	movq	%r14, -48(%rbp)
	movl	-40(%rbp), %edi
	movq	-56(%rbp), %rsi
	movq	-48(%rbp), %rdx
	callq	PMPI_Cart_sub
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_82, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end81:
	.size	MPI_Cart_sub, .Lfunc_end81-MPI_Cart_sub
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Cartdim_get         # -- Begin function MPI_Cartdim_get
	.p2align	4, 0x90
	.type	MPI_Cartdim_get,@function
MPI_Cartdim_get:                        # @MPI_Cartdim_get
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$82, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Cartdim_get
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_83, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end82:
	.size	MPI_Cartdim_get, .Lfunc_end82-MPI_Cartdim_get
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Dims_create         # -- Begin function MPI_Dims_create
	.p2align	4, 0x90
	.type	MPI_Dims_create,@function
MPI_Dims_create:                        # @MPI_Dims_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$83, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Dims_create
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_84, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end83:
	.size	MPI_Dims_create, .Lfunc_end83-MPI_Dims_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Graph_create        # -- Begin function MPI_Graph_create
	.p2align	4, 0x90
	.type	MPI_Graph_create,@function
MPI_Graph_create:                       # @MPI_Graph_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -64(%rbp)          # 8-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movq	%rdx, %r13
	movl	%esi, %ebx
	movl	%edi, %r14d
	movl	$84, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movl	%r14d, -56(%rbp)
	movl	%ebx, -52(%rbp)
	movq	%r13, -96(%rbp)
	movq	%r12, -88(%rbp)
	movl	%r15d, -48(%rbp)
	movq	-64(%rbp), %rax         # 8-byte Reload
	movq	%rax, -80(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movq	-96(%rbp), %rdx
	movq	-88(%rbp), %rcx
	movl	-48(%rbp), %r8d
	movq	-80(%rbp), %r9
	callq	PMPI_Graph_create
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_85, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end84:
	.size	MPI_Graph_create, .Lfunc_end84-MPI_Graph_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Graph_get           # -- Begin function MPI_Graph_get
	.p2align	4, 0x90
	.type	MPI_Graph_get,@function
MPI_Graph_get:                          # @MPI_Graph_get
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movl	%edx, %r12d
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$85, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -56(%rbp)
	movl	%r13d, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -80(%rbp)
	movq	%r14, -72(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-80(%rbp), %rcx
	movq	-72(%rbp), %r8
	callq	PMPI_Graph_get
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_86, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end85:
	.size	MPI_Graph_get, .Lfunc_end85-MPI_Graph_get
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Graph_map           # -- Begin function MPI_Graph_map
	.p2align	4, 0x90
	.type	MPI_Graph_map,@function
MPI_Graph_map:                          # @MPI_Graph_map
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movq	%rdx, %r12
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$86, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -52(%rbp)
	movl	%r13d, -48(%rbp)
	movq	%r12, -88(%rbp)
	movq	%r15, -80(%rbp)
	movq	%r14, -72(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-88(%rbp), %rdx
	movq	-80(%rbp), %rcx
	movq	-72(%rbp), %r8
	callq	PMPI_Graph_map
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_87, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end86:
	.size	MPI_Graph_map, .Lfunc_end86-MPI_Graph_map
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Graph_neighbors     # -- Begin function MPI_Graph_neighbors
	.p2align	4, 0x90
	.type	MPI_Graph_neighbors,@function
MPI_Graph_neighbors:                    # @MPI_Graph_neighbors
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movl	%edx, %r15d
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$87, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -56(%rbp)
	movl	%r12d, -52(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -64(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-64(%rbp), %rcx
	callq	PMPI_Graph_neighbors
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_88, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end87:
	.size	MPI_Graph_neighbors, .Lfunc_end87-MPI_Graph_neighbors
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Graph_neighbors_count # -- Begin function MPI_Graph_neighbors_count
	.p2align	4, 0x90
	.type	MPI_Graph_neighbors_count,@function
MPI_Graph_neighbors_count:              # @MPI_Graph_neighbors_count
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$88, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Graph_neighbors_count
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_89, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end88:
	.size	MPI_Graph_neighbors_count, .Lfunc_end88-MPI_Graph_neighbors_count
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Graphdims_get       # -- Begin function MPI_Graphdims_get
	.p2align	4, 0x90
	.type	MPI_Graphdims_get,@function
MPI_Graphdims_get:                      # @MPI_Graphdims_get
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movq	%rsi, %r15
	movl	%edi, %ebx
	movl	$89, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -40(%rbp)
	movq	%r15, -56(%rbp)
	movq	%r14, -48(%rbp)
	movl	-40(%rbp), %edi
	movq	-56(%rbp), %rsi
	movq	-48(%rbp), %rdx
	callq	PMPI_Graphdims_get
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_90, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end89:
	.size	MPI_Graphdims_get, .Lfunc_end89-MPI_Graphdims_get
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Topo_test           # -- Begin function MPI_Topo_test
	.p2align	4, 0x90
	.type	MPI_Topo_test,@function
MPI_Topo_test:                          # @MPI_Topo_test
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$90, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Topo_test
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_91, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end90:
	.size	MPI_Topo_test, .Lfunc_end90-MPI_Topo_test
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Abort               # -- Begin function MPI_Abort
	.p2align	4, 0x90
	.type	MPI_Abort,@function
MPI_Abort:                              # @MPI_Abort
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%esi, %r14d
	movl	%edi, %ebx
	movl	$91, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -36(%rbp)
	movl	%r14d, -32(%rbp)
	movl	-36(%rbp), %edi
	movl	-32(%rbp), %esi
	callq	PMPI_Abort
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_92, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end91:
	.size	MPI_Abort, .Lfunc_end91-MPI_Abort
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Error_class         # -- Begin function MPI_Error_class
	.p2align	4, 0x90
	.type	MPI_Error_class,@function
MPI_Error_class:                        # @MPI_Error_class
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$92, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Error_class
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_93, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end92:
	.size	MPI_Error_class, .Lfunc_end92-MPI_Error_class
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Errhandler_create   # -- Begin function MPI_Errhandler_create
	.p2align	4, 0x90
	.type	MPI_Errhandler_create,@function
MPI_Errhandler_create:                  # @MPI_Errhandler_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movq	%rdi, %rbx
	movl	$93, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -48(%rbp)
	movq	%r14, -40(%rbp)
	movq	-48(%rbp), %rdi
	movq	-40(%rbp), %rsi
	callq	PMPI_Errhandler_create
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_94, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end93:
	.size	MPI_Errhandler_create, .Lfunc_end93-MPI_Errhandler_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Errhandler_free     # -- Begin function MPI_Errhandler_free
	.p2align	4, 0x90
	.type	MPI_Errhandler_free,@function
MPI_Errhandler_free:                    # @MPI_Errhandler_free
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$94, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Errhandler_free
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_95, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end94:
	.size	MPI_Errhandler_free, .Lfunc_end94-MPI_Errhandler_free
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Errhandler_get      # -- Begin function MPI_Errhandler_get
	.p2align	4, 0x90
	.type	MPI_Errhandler_get,@function
MPI_Errhandler_get:                     # @MPI_Errhandler_get
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$95, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Errhandler_get
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_96, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end95:
	.size	MPI_Errhandler_get, .Lfunc_end95-MPI_Errhandler_get
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Error_string        # -- Begin function MPI_Error_string
	.p2align	4, 0x90
	.type	MPI_Error_string,@function
MPI_Error_string:                       # @MPI_Error_string
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movq	%rsi, %r15
	movl	%edi, %ebx
	movl	$96, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -40(%rbp)
	movq	%r15, -56(%rbp)
	movq	%r14, -48(%rbp)
	movl	-40(%rbp), %edi
	movq	-56(%rbp), %rsi
	movq	-48(%rbp), %rdx
	callq	PMPI_Error_string
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_97, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end96:
	.size	MPI_Error_string, .Lfunc_end96-MPI_Error_string
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Errhandler_set      # -- Begin function MPI_Errhandler_set
	.p2align	4, 0x90
	.type	MPI_Errhandler_set,@function
MPI_Errhandler_set:                     # @MPI_Errhandler_set
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%esi, %r14d
	movl	%edi, %ebx
	movl	$97, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -36(%rbp)
	movl	%r14d, -32(%rbp)
	movl	-36(%rbp), %edi
	movl	-32(%rbp), %esi
	callq	PMPI_Errhandler_set
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_98, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end97:
	.size	MPI_Errhandler_set, .Lfunc_end97-MPI_Errhandler_set
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Get_processor_name  # -- Begin function MPI_Get_processor_name
	.p2align	4, 0x90
	.type	MPI_Get_processor_name,@function
MPI_Get_processor_name:                 # @MPI_Get_processor_name
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movq	%rdi, %rbx
	movl	$98, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -48(%rbp)
	movq	%r14, -40(%rbp)
	movq	-48(%rbp), %rdi
	movq	-40(%rbp), %rsi
	callq	PMPI_Get_processor_name
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_99, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end98:
	.size	MPI_Get_processor_name, .Lfunc_end98-MPI_Get_processor_name
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Wtick               # -- Begin function MPI_Wtick
	.p2align	4, 0x90
	.type	MPI_Wtick,@function
MPI_Wtick:                              # @MPI_Wtick
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -24
	movl	$99, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %rbx
	callq	PMPI_Wtick
	movsd	%xmm0, -24(%rbp)
	movsd	-24(%rbp), %xmm0        # xmm0 = mem[0],zero
	movsd	%xmm0, -16(%rbp)        # 8-byte Spill
	movabsq	$.L__unnamed_100, %rdi
	movq	%rbx, %rsi
	callq	__profile__record_time_end
	movsd	-16(%rbp), %xmm0        # 8-byte Reload
                                        # xmm0 = mem[0],zero
	addq	$56, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end99:
	.size	MPI_Wtick, .Lfunc_end99-MPI_Wtick
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Wtime               # -- Begin function MPI_Wtime
	.p2align	4, 0x90
	.type	MPI_Wtime,@function
MPI_Wtime:                              # @MPI_Wtime
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -24
	movl	$100, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %rbx
	callq	PMPI_Wtime
	movsd	%xmm0, -24(%rbp)
	movsd	-24(%rbp), %xmm0        # xmm0 = mem[0],zero
	movsd	%xmm0, -16(%rbp)        # 8-byte Spill
	movabsq	$.L__unnamed_101, %rdi
	movq	%rbx, %rsi
	callq	__profile__record_time_end
	movsd	-16(%rbp), %xmm0        # 8-byte Reload
                                        # xmm0 = mem[0],zero
	addq	$56, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end100:
	.size	MPI_Wtime, .Lfunc_end100-MPI_Wtime
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Address             # -- Begin function MPI_Address
	.p2align	4, 0x90
	.type	MPI_Address,@function
MPI_Address:                            # @MPI_Address
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movq	%rdi, %rbx
	movl	$101, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -48(%rbp)
	movq	%r14, -40(%rbp)
	movq	-48(%rbp), %rdi
	movq	-40(%rbp), %rsi
	callq	PMPI_Address
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_102, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end101:
	.size	MPI_Address, .Lfunc_end101-MPI_Address
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Op_create           # -- Begin function MPI_Op_create
	.p2align	4, 0x90
	.type	MPI_Op_create,@function
MPI_Op_create:                          # @MPI_Op_create
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movq	%rdi, %rbx
	movl	$102, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movq	%rbx, -56(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -48(%rbp)
	movq	-56(%rbp), %rdi
	movl	-40(%rbp), %esi
	movq	-48(%rbp), %rdx
	callq	PMPI_Op_create
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_103, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end102:
	.size	MPI_Op_create, .Lfunc_end102-MPI_Op_create
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Op_free             # -- Begin function MPI_Op_free
	.p2align	4, 0x90
	.type	MPI_Op_free,@function
MPI_Op_free:                            # @MPI_Op_free
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$103, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Op_free
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_104, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end103:
	.size	MPI_Op_free, .Lfunc_end103-MPI_Op_free
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Attr_delete         # -- Begin function MPI_Attr_delete
	.p2align	4, 0x90
	.type	MPI_Attr_delete,@function
MPI_Attr_delete:                        # @MPI_Attr_delete
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%esi, %r14d
	movl	%edi, %ebx
	movl	$104, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -36(%rbp)
	movl	%r14d, -32(%rbp)
	movl	-36(%rbp), %edi
	movl	-32(%rbp), %esi
	callq	PMPI_Attr_delete
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_105, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end104:
	.size	MPI_Attr_delete, .Lfunc_end104-MPI_Attr_delete
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Attr_get            # -- Begin function MPI_Attr_get
	.p2align	4, 0x90
	.type	MPI_Attr_get,@function
MPI_Attr_get:                           # @MPI_Attr_get
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movq	%rdx, %r15
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$105, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -52(%rbp)
	movl	%r12d, -48(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-52(%rbp), %edi
	movl	-48(%rbp), %esi
	movq	-72(%rbp), %rdx
	movq	-64(%rbp), %rcx
	callq	PMPI_Attr_get
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_106, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end105:
	.size	MPI_Attr_get, .Lfunc_end105-MPI_Attr_get
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Attr_put            # -- Begin function MPI_Attr_put
	.p2align	4, 0x90
	.type	MPI_Attr_put,@function
MPI_Attr_put:                           # @MPI_Attr_put
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$106, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Attr_put
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_107, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end106:
	.size	MPI_Attr_put, .Lfunc_end106-MPI_Attr_put
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Buffer_attach       # -- Begin function MPI_Buffer_attach
	.p2align	4, 0x90
	.type	MPI_Buffer_attach,@function
MPI_Buffer_attach:                      # @MPI_Buffer_attach
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%esi, %r14d
	movq	%rdi, %rbx
	movl	$107, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -40(%rbp)
	movl	%r14d, -32(%rbp)
	movq	-40(%rbp), %rdi
	movl	-32(%rbp), %esi
	callq	PMPI_Buffer_attach
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_108, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end107:
	.size	MPI_Buffer_attach, .Lfunc_end107-MPI_Buffer_attach
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Buffer_detach       # -- Begin function MPI_Buffer_detach
	.p2align	4, 0x90
	.type	MPI_Buffer_detach,@function
MPI_Buffer_detach:                      # @MPI_Buffer_detach
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movq	%rdi, %rbx
	movl	$108, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movq	%rbx, -48(%rbp)
	movq	%r14, -40(%rbp)
	movq	-48(%rbp), %rdi
	movq	-40(%rbp), %rsi
	callq	PMPI_Buffer_detach
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_109, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end108:
	.size	MPI_Buffer_detach, .Lfunc_end108-MPI_Buffer_detach
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Get_elements        # -- Begin function MPI_Get_elements
	.p2align	4, 0x90
	.type	MPI_Get_elements,@function
MPI_Get_elements:                       # @MPI_Get_elements
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movq	%rdi, %rbx
	movl	$109, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movq	%rbx, -56(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -48(%rbp)
	movq	-56(%rbp), %rdi
	movl	-40(%rbp), %esi
	movq	-48(%rbp), %rdx
	callq	PMPI_Get_elements
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_110, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end109:
	.size	MPI_Get_elements, .Lfunc_end109-MPI_Get_elements
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Get_count           # -- Begin function MPI_Get_count
	.p2align	4, 0x90
	.type	MPI_Get_count,@function
MPI_Get_count:                          # @MPI_Get_count
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movq	%rdi, %rbx
	movl	$110, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movq	%rbx, -56(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -48(%rbp)
	movq	-56(%rbp), %rdi
	movl	-40(%rbp), %esi
	movq	-48(%rbp), %rdx
	callq	PMPI_Get_count
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_111, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end110:
	.size	MPI_Get_count, .Lfunc_end110-MPI_Get_count
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_commit         # -- Begin function MPI_Type_commit
	.p2align	4, 0x90
	.type	MPI_Type_commit,@function
MPI_Type_commit:                        # @MPI_Type_commit
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$111, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Type_commit
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_112, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end111:
	.size	MPI_Type_commit, .Lfunc_end111-MPI_Type_commit
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_contiguous     # -- Begin function MPI_Type_contiguous
	.p2align	4, 0x90
	.type	MPI_Type_contiguous,@function
MPI_Type_contiguous:                    # @MPI_Type_contiguous
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r12
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdx, %r14
	movl	%esi, %r15d
	movl	%edi, %ebx
	movl	$112, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r12
	movl	%ebx, -44(%rbp)
	movl	%r15d, -40(%rbp)
	movq	%r14, -56(%rbp)
	movl	-44(%rbp), %edi
	movl	-40(%rbp), %esi
	movq	-56(%rbp), %rdx
	callq	PMPI_Type_contiguous
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %ebx
	movabsq	$.L__unnamed_113, %rdi
	movq	%r12, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r12
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end112:
	.size	MPI_Type_contiguous, .Lfunc_end112-MPI_Type_contiguous
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_extent         # -- Begin function MPI_Type_extent
	.p2align	4, 0x90
	.type	MPI_Type_extent,@function
MPI_Type_extent:                        # @MPI_Type_extent
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$113, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Type_extent
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_114, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end113:
	.size	MPI_Type_extent, .Lfunc_end113-MPI_Type_extent
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_free           # -- Begin function MPI_Type_free
	.p2align	4, 0x90
	.type	MPI_Type_free,@function
MPI_Type_free:                          # @MPI_Type_free
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$64, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	movl	$114, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r14
	movq	%rbx, -32(%rbp)
	movq	-32(%rbp), %rdi
	callq	PMPI_Type_free
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %ebx
	movabsq	$.L__unnamed_115, %rdi
	movq	%r14, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$64, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end114:
	.size	MPI_Type_free, .Lfunc_end114-MPI_Type_free
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_hindexed       # -- Begin function MPI_Type_hindexed
	.p2align	4, 0x90
	.type	MPI_Type_hindexed,@function
MPI_Type_hindexed:                      # @MPI_Type_hindexed
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movl	%ecx, %r15d
	movq	%rdx, %r12
	movq	%rsi, %r13
	movl	%edi, %ebx
	movl	$115, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -52(%rbp)
	movq	%r13, -88(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -72(%rbp)
	movl	-52(%rbp), %edi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movl	-48(%rbp), %ecx
	movq	-72(%rbp), %r8
	callq	PMPI_Type_hindexed
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_116, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end115:
	.size	MPI_Type_hindexed, .Lfunc_end115-MPI_Type_hindexed
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_hvector        # -- Begin function MPI_Type_hvector
	.p2align	4, 0x90
	.type	MPI_Type_hvector,@function
MPI_Type_hvector:                       # @MPI_Type_hvector
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movl	%ecx, %r15d
	movq	%rdx, %r12
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$116, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -56(%rbp)
	movl	%r13d, -52(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -72(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movq	-80(%rbp), %rdx
	movl	-48(%rbp), %ecx
	movq	-72(%rbp), %r8
	callq	PMPI_Type_hvector
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_117, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end116:
	.size	MPI_Type_hvector, .Lfunc_end116-MPI_Type_hvector
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_indexed        # -- Begin function MPI_Type_indexed
	.p2align	4, 0x90
	.type	MPI_Type_indexed,@function
MPI_Type_indexed:                       # @MPI_Type_indexed
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movl	%ecx, %r15d
	movq	%rdx, %r12
	movq	%rsi, %r13
	movl	%edi, %ebx
	movl	$117, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -64(%rbp)         # 8-byte Spill
	movl	%ebx, -52(%rbp)
	movq	%r13, -88(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -72(%rbp)
	movl	-52(%rbp), %edi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movl	-48(%rbp), %ecx
	movq	-72(%rbp), %r8
	callq	PMPI_Type_indexed
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_118, %rdi
	movq	-64(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end117:
	.size	MPI_Type_indexed, .Lfunc_end117-MPI_Type_indexed
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_lb             # -- Begin function MPI_Type_lb
	.p2align	4, 0x90
	.type	MPI_Type_lb,@function
MPI_Type_lb:                            # @MPI_Type_lb
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$118, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Type_lb
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_119, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end118:
	.size	MPI_Type_lb, .Lfunc_end118-MPI_Type_lb
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_size           # -- Begin function MPI_Type_size
	.p2align	4, 0x90
	.type	MPI_Type_size,@function
MPI_Type_size:                          # @MPI_Type_size
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$119, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Type_size
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_120, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end119:
	.size	MPI_Type_size, .Lfunc_end119-MPI_Type_size
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_struct         # -- Begin function MPI_Type_struct
	.p2align	4, 0x90
	.type	MPI_Type_struct,@function
MPI_Type_struct:                        # @MPI_Type_struct
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movq	%rcx, %r15
	movq	%rdx, %r12
	movq	%rsi, %r13
	movl	%edi, %ebx
	movl	$120, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -56(%rbp)         # 8-byte Spill
	movl	%ebx, -48(%rbp)
	movq	%r13, -88(%rbp)
	movq	%r12, -80(%rbp)
	movq	%r15, -72(%rbp)
	movq	%r14, -64(%rbp)
	movl	-48(%rbp), %edi
	movq	-88(%rbp), %rsi
	movq	-80(%rbp), %rdx
	movq	-72(%rbp), %rcx
	movq	-64(%rbp), %r8
	callq	PMPI_Type_struct
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_121, %rdi
	movq	-56(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end120:
	.size	MPI_Type_struct, .Lfunc_end120-MPI_Type_struct
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_ub             # -- Begin function MPI_Type_ub
	.p2align	4, 0x90
	.type	MPI_Type_ub,@function
MPI_Type_ub:                            # @MPI_Type_ub
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$56, %rsp
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rsi, %r14
	movl	%edi, %ebx
	movl	$121, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r15
	movl	%ebx, -32(%rbp)
	movq	%r14, -40(%rbp)
	movl	-32(%rbp), %edi
	movq	-40(%rbp), %rsi
	callq	PMPI_Type_ub
	movl	%eax, -28(%rbp)
	movl	-28(%rbp), %ebx
	movabsq	$.L__unnamed_122, %rdi
	movq	%r15, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$56, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end121:
	.size	MPI_Type_ub, .Lfunc_end121-MPI_Type_ub
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Type_vector         # -- Begin function MPI_Type_vector
	.p2align	4, 0x90
	.type	MPI_Type_vector,@function
MPI_Type_vector:                        # @MPI_Type_vector
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$88, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r8, %r14
	movl	%ecx, %r15d
	movl	%edx, %r12d
	movl	%esi, %r13d
	movl	%edi, %ebx
	movl	$122, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movl	%ebx, -60(%rbp)
	movl	%r13d, -56(%rbp)
	movl	%r12d, -52(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -80(%rbp)
	movl	-60(%rbp), %edi
	movl	-56(%rbp), %esi
	movl	-52(%rbp), %edx
	movl	-48(%rbp), %ecx
	movq	-80(%rbp), %r8
	callq	PMPI_Type_vector
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_123, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$88, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end122:
	.size	MPI_Type_vector, .Lfunc_end122-MPI_Type_vector
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Unpack              # -- Begin function MPI_Unpack
	.p2align	4, 0x90
	.type	MPI_Unpack,@function
MPI_Unpack:                             # @MPI_Unpack
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movl	%r9d, -44(%rbp)         # 4-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movq	%rdx, %r13
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	16(%rbp), %eax
	movl	$123, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -96(%rbp)
	movl	%ebx, -60(%rbp)
	movq	%r13, -88(%rbp)
	movq	%r12, -80(%rbp)
	movl	%r15d, -56(%rbp)
	movl	-44(%rbp), %eax         # 4-byte Reload
	movl	%eax, -52(%rbp)
	movq	-96(%rbp), %rdi
	movl	-60(%rbp), %esi
	movq	-88(%rbp), %rdx
	movq	-80(%rbp), %rcx
	movl	-56(%rbp), %r8d
	movl	-52(%rbp), %r9d
	movl	16(%rbp), %eax
	movl	%eax, (%rsp)
	callq	PMPI_Unpack
	movl	%eax, -48(%rbp)
	movl	-48(%rbp), %ebx
	movabsq	$.L__unnamed_124, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end123:
	.size	MPI_Unpack, .Lfunc_end123-MPI_Unpack
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Pack                # -- Begin function MPI_Pack
	.p2align	4, 0x90
	.type	MPI_Pack,@function
MPI_Pack:                               # @MPI_Pack
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%r9, -64(%rbp)          # 8-byte Spill
	movl	%r8d, %r15d
	movq	%rcx, %r12
	movl	%edx, %r13d
	movl	%esi, %ebx
	movq	%rdi, %r14
	movl	16(%rbp), %eax
	movl	$124, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, -72(%rbp)         # 8-byte Spill
	movq	%r14, -96(%rbp)
	movl	%ebx, -56(%rbp)
	movl	%r13d, -52(%rbp)
	movq	%r12, -88(%rbp)
	movl	%r15d, -48(%rbp)
	movq	-64(%rbp), %rax         # 8-byte Reload
	movq	%rax, -80(%rbp)
	movq	-96(%rbp), %rdi
	movl	-56(%rbp), %esi
	movl	-52(%rbp), %edx
	movq	-88(%rbp), %rcx
	movl	-48(%rbp), %r8d
	movq	-80(%rbp), %r9
	movl	16(%rbp), %eax
	movl	%eax, (%rsp)
	callq	PMPI_Pack
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_125, %rdi
	movq	-72(%rbp), %rsi         # 8-byte Reload
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$104, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end124:
	.size	MPI_Pack, .Lfunc_end124-MPI_Pack
	.cfi_endproc
                                        # -- End function
	.globl	MPI_Pack_size           # -- Begin function MPI_Pack_size
	.p2align	4, 0x90
	.type	MPI_Pack_size,@function
MPI_Pack_size:                          # @MPI_Pack_size
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rcx, %r14
	movl	%edx, %r15d
	movl	%esi, %r12d
	movl	%edi, %ebx
	movl	$125, __profile__funcID
	callq	__profile__record_time_begin
	movq	%rax, %r13
	movl	%ebx, -56(%rbp)
	movl	%r12d, -52(%rbp)
	movl	%r15d, -48(%rbp)
	movq	%r14, -64(%rbp)
	movl	-56(%rbp), %edi
	movl	-52(%rbp), %esi
	movl	-48(%rbp), %edx
	movq	-64(%rbp), %rcx
	callq	PMPI_Pack_size
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %ebx
	movabsq	$.L__unnamed_126, %rdi
	movq	%r13, %rsi
	callq	__profile__record_time_end
	movl	%ebx, %eax
	addq	$72, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end125:
	.size	MPI_Pack_size, .Lfunc_end125-MPI_Pack_size
	.cfi_endproc
                                        # -- End function
	.type	.L__unnamed_1,@object   # @0
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_1:
	.asciz	"MPI_Init"
	.size	.L__unnamed_1, 9

	.type	.L__unnamed_2,@object   # @1
.L__unnamed_2:
	.asciz	"MPI_Finalize"
	.size	.L__unnamed_2, 13

	.type	.L__unnamed_3,@object   # @2
.L__unnamed_3:
	.asciz	"MPI_Bsend"
	.size	.L__unnamed_3, 10

	.type	.L__unnamed_4,@object   # @3
.L__unnamed_4:
	.asciz	"MPI_Bsend_init"
	.size	.L__unnamed_4, 15

	.type	.L__unnamed_5,@object   # @4
.L__unnamed_5:
	.asciz	"MPI_Recv_init"
	.size	.L__unnamed_5, 14

	.type	.L__unnamed_6,@object   # @5
.L__unnamed_6:
	.asciz	"MPI_Send_init"
	.size	.L__unnamed_6, 14

	.type	.L__unnamed_7,@object   # @6
.L__unnamed_7:
	.asciz	"MPI_Ibsend"
	.size	.L__unnamed_7, 11

	.type	.L__unnamed_8,@object   # @7
.L__unnamed_8:
	.asciz	"MPI_Irecv"
	.size	.L__unnamed_8, 10

	.type	.L__unnamed_9,@object   # @8
.L__unnamed_9:
	.asciz	"MPI_Irsend"
	.size	.L__unnamed_9, 11

	.type	.L__unnamed_10,@object  # @9
.L__unnamed_10:
	.asciz	"MPI_Isend"
	.size	.L__unnamed_10, 10

	.type	.L__unnamed_11,@object  # @10
.L__unnamed_11:
	.asciz	"MPI_Issend"
	.size	.L__unnamed_11, 11

	.type	.L__unnamed_12,@object  # @11
.L__unnamed_12:
	.asciz	"MPI_Recv"
	.size	.L__unnamed_12, 9

	.type	.L__unnamed_13,@object  # @12
.L__unnamed_13:
	.asciz	"MPI_Rsend"
	.size	.L__unnamed_13, 10

	.type	.L__unnamed_14,@object  # @13
.L__unnamed_14:
	.asciz	"MPI_Rsend_init"
	.size	.L__unnamed_14, 15

	.type	.L__unnamed_15,@object  # @14
.L__unnamed_15:
	.asciz	"MPI_Send"
	.size	.L__unnamed_15, 9

	.type	.L__unnamed_16,@object  # @15
.L__unnamed_16:
	.asciz	"MPI_Sendrecv"
	.size	.L__unnamed_16, 13

	.type	.L__unnamed_17,@object  # @16
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_17:
	.asciz	"MPI_Sendrecv_replace"
	.size	.L__unnamed_17, 21

	.type	.L__unnamed_18,@object  # @17
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_18:
	.asciz	"MPI_Ssend"
	.size	.L__unnamed_18, 10

	.type	.L__unnamed_19,@object  # @18
.L__unnamed_19:
	.asciz	"MPI_Ssend_init"
	.size	.L__unnamed_19, 15

	.type	.L__unnamed_20,@object  # @19
.L__unnamed_20:
	.asciz	"MPI_Test"
	.size	.L__unnamed_20, 9

	.type	.L__unnamed_21,@object  # @20
.L__unnamed_21:
	.asciz	"MPI_Testall"
	.size	.L__unnamed_21, 12

	.type	.L__unnamed_22,@object  # @21
.L__unnamed_22:
	.asciz	"MPI_Testany"
	.size	.L__unnamed_22, 12

	.type	.L__unnamed_23,@object  # @22
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_23:
	.asciz	"MPI_Test_cancelled"
	.size	.L__unnamed_23, 19

	.type	.L__unnamed_24,@object  # @23
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_24:
	.asciz	"MPI_Testsome"
	.size	.L__unnamed_24, 13

	.type	.L__unnamed_25,@object  # @24
.L__unnamed_25:
	.asciz	"MPI_Wait"
	.size	.L__unnamed_25, 9

	.type	.L__unnamed_26,@object  # @25
.L__unnamed_26:
	.asciz	"MPI_Waitall"
	.size	.L__unnamed_26, 12

	.type	.L__unnamed_27,@object  # @26
.L__unnamed_27:
	.asciz	"MPI_Waitany"
	.size	.L__unnamed_27, 12

	.type	.L__unnamed_28,@object  # @27
.L__unnamed_28:
	.asciz	"MPI_Waitsome"
	.size	.L__unnamed_28, 13

	.type	.L__unnamed_29,@object  # @28
.L__unnamed_29:
	.asciz	"MPI_Cancel"
	.size	.L__unnamed_29, 11

	.type	.L__unnamed_30,@object  # @29
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_30:
	.asciz	"MPI_Request_free"
	.size	.L__unnamed_30, 17

	.type	.L__unnamed_31,@object  # @30
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_31:
	.asciz	"MPI_Start"
	.size	.L__unnamed_31, 10

	.type	.L__unnamed_32,@object  # @31
.L__unnamed_32:
	.asciz	"MPI_Startall"
	.size	.L__unnamed_32, 13

	.type	.L__unnamed_33,@object  # @32
.L__unnamed_33:
	.asciz	"MPI_Iprobe"
	.size	.L__unnamed_33, 11

	.type	.L__unnamed_34,@object  # @33
.L__unnamed_34:
	.asciz	"MPI_Probe"
	.size	.L__unnamed_34, 10

	.type	.L__unnamed_35,@object  # @34
.L__unnamed_35:
	.asciz	"MPI_Allgather"
	.size	.L__unnamed_35, 14

	.type	.L__unnamed_36,@object  # @35
.L__unnamed_36:
	.asciz	"MPI_Allgatherv"
	.size	.L__unnamed_36, 15

	.type	.L__unnamed_37,@object  # @36
.L__unnamed_37:
	.asciz	"MPI_Allreduce"
	.size	.L__unnamed_37, 14

	.type	.L__unnamed_38,@object  # @37
.L__unnamed_38:
	.asciz	"MPI_Alltoall"
	.size	.L__unnamed_38, 13

	.type	.L__unnamed_39,@object  # @38
.L__unnamed_39:
	.asciz	"MPI_Alltoallv"
	.size	.L__unnamed_39, 14

	.type	.L__unnamed_40,@object  # @39
.L__unnamed_40:
	.asciz	"MPI_Barrier"
	.size	.L__unnamed_40, 12

	.type	.L__unnamed_41,@object  # @40
.L__unnamed_41:
	.asciz	"MPI_Bcast"
	.size	.L__unnamed_41, 10

	.type	.L__unnamed_42,@object  # @41
.L__unnamed_42:
	.asciz	"MPI_Gather"
	.size	.L__unnamed_42, 11

	.type	.L__unnamed_43,@object  # @42
.L__unnamed_43:
	.asciz	"MPI_Gatherv"
	.size	.L__unnamed_43, 12

	.type	.L__unnamed_44,@object  # @43
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_44:
	.asciz	"MPI_Reduce_scatter"
	.size	.L__unnamed_44, 19

	.type	.L__unnamed_45,@object  # @44
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_45:
	.asciz	"MPI_Reduce"
	.size	.L__unnamed_45, 11

	.type	.L__unnamed_46,@object  # @45
.L__unnamed_46:
	.asciz	"MPI_Scan"
	.size	.L__unnamed_46, 9

	.type	.L__unnamed_47,@object  # @46
.L__unnamed_47:
	.asciz	"MPI_Scatter"
	.size	.L__unnamed_47, 12

	.type	.L__unnamed_48,@object  # @47
.L__unnamed_48:
	.asciz	"MPI_Scatterv"
	.size	.L__unnamed_48, 13

	.type	.L__unnamed_49,@object  # @48
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_49:
	.asciz	"MPI_Comm_compare"
	.size	.L__unnamed_49, 17

	.type	.L__unnamed_50,@object  # @49
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_50:
	.asciz	"MPI_Comm_create"
	.size	.L__unnamed_50, 16

	.type	.L__unnamed_51,@object  # @50
.L__unnamed_51:
	.asciz	"MPI_Comm_dup"
	.size	.L__unnamed_51, 13

	.type	.L__unnamed_52,@object  # @51
.L__unnamed_52:
	.asciz	"MPI_Comm_free"
	.size	.L__unnamed_52, 14

	.type	.L__unnamed_53,@object  # @52
.L__unnamed_53:
	.asciz	"MPI_Comm_group"
	.size	.L__unnamed_53, 15

	.type	.L__unnamed_54,@object  # @53
.L__unnamed_54:
	.asciz	"MPI_Comm_rank"
	.size	.L__unnamed_54, 14

	.type	.L__unnamed_55,@object  # @54
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_55:
	.asciz	"MPI_Comm_remote_group"
	.size	.L__unnamed_55, 22

	.type	.L__unnamed_56,@object  # @55
	.p2align	4
.L__unnamed_56:
	.asciz	"MPI_Comm_remote_size"
	.size	.L__unnamed_56, 21

	.type	.L__unnamed_57,@object  # @56
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_57:
	.asciz	"MPI_Comm_size"
	.size	.L__unnamed_57, 14

	.type	.L__unnamed_58,@object  # @57
.L__unnamed_58:
	.asciz	"MPI_Comm_split"
	.size	.L__unnamed_58, 15

	.type	.L__unnamed_59,@object  # @58
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_59:
	.asciz	"MPI_Comm_test_inter"
	.size	.L__unnamed_59, 20

	.type	.L__unnamed_60,@object  # @59
	.p2align	4
.L__unnamed_60:
	.asciz	"MPI_Group_compare"
	.size	.L__unnamed_60, 18

	.type	.L__unnamed_61,@object  # @60
	.p2align	4
.L__unnamed_61:
	.asciz	"MPI_Group_difference"
	.size	.L__unnamed_61, 21

	.type	.L__unnamed_62,@object  # @61
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_62:
	.asciz	"MPI_Group_excl"
	.size	.L__unnamed_62, 15

	.type	.L__unnamed_63,@object  # @62
.L__unnamed_63:
	.asciz	"MPI_Group_free"
	.size	.L__unnamed_63, 15

	.type	.L__unnamed_64,@object  # @63
.L__unnamed_64:
	.asciz	"MPI_Group_incl"
	.size	.L__unnamed_64, 15

	.type	.L__unnamed_65,@object  # @64
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_65:
	.asciz	"MPI_Group_intersection"
	.size	.L__unnamed_65, 23

	.type	.L__unnamed_66,@object  # @65
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_66:
	.asciz	"MPI_Group_rank"
	.size	.L__unnamed_66, 15

	.type	.L__unnamed_67,@object  # @66
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_67:
	.asciz	"MPI_Group_range_excl"
	.size	.L__unnamed_67, 21

	.type	.L__unnamed_68,@object  # @67
	.p2align	4
.L__unnamed_68:
	.asciz	"MPI_Group_range_incl"
	.size	.L__unnamed_68, 21

	.type	.L__unnamed_69,@object  # @68
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_69:
	.asciz	"MPI_Group_size"
	.size	.L__unnamed_69, 15

	.type	.L__unnamed_70,@object  # @69
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_70:
	.asciz	"MPI_Group_translate_ranks"
	.size	.L__unnamed_70, 26

	.type	.L__unnamed_71,@object  # @70
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_71:
	.asciz	"MPI_Group_union"
	.size	.L__unnamed_71, 16

	.type	.L__unnamed_72,@object  # @71
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_72:
	.asciz	"MPI_Intercomm_create"
	.size	.L__unnamed_72, 21

	.type	.L__unnamed_73,@object  # @72
	.p2align	4
.L__unnamed_73:
	.asciz	"MPI_Intercomm_merge"
	.size	.L__unnamed_73, 20

	.type	.L__unnamed_74,@object  # @73
	.p2align	4
.L__unnamed_74:
	.asciz	"MPI_Keyval_create"
	.size	.L__unnamed_74, 18

	.type	.L__unnamed_75,@object  # @74
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_75:
	.asciz	"MPI_Keyval_free"
	.size	.L__unnamed_75, 16

	.type	.L__unnamed_76,@object  # @75
.L__unnamed_76:
	.asciz	"MPI_Cart_coords"
	.size	.L__unnamed_76, 16

	.type	.L__unnamed_77,@object  # @76
.L__unnamed_77:
	.asciz	"MPI_Cart_create"
	.size	.L__unnamed_77, 16

	.type	.L__unnamed_78,@object  # @77
.L__unnamed_78:
	.asciz	"MPI_Cart_get"
	.size	.L__unnamed_78, 13

	.type	.L__unnamed_79,@object  # @78
.L__unnamed_79:
	.asciz	"MPI_Cart_map"
	.size	.L__unnamed_79, 13

	.type	.L__unnamed_80,@object  # @79
.L__unnamed_80:
	.asciz	"MPI_Cart_rank"
	.size	.L__unnamed_80, 14

	.type	.L__unnamed_81,@object  # @80
.L__unnamed_81:
	.asciz	"MPI_Cart_shift"
	.size	.L__unnamed_81, 15

	.type	.L__unnamed_82,@object  # @81
.L__unnamed_82:
	.asciz	"MPI_Cart_sub"
	.size	.L__unnamed_82, 13

	.type	.L__unnamed_83,@object  # @82
.L__unnamed_83:
	.asciz	"MPI_Cartdim_get"
	.size	.L__unnamed_83, 16

	.type	.L__unnamed_84,@object  # @83
.L__unnamed_84:
	.asciz	"MPI_Dims_create"
	.size	.L__unnamed_84, 16

	.type	.L__unnamed_85,@object  # @84
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_85:
	.asciz	"MPI_Graph_create"
	.size	.L__unnamed_85, 17

	.type	.L__unnamed_86,@object  # @85
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_86:
	.asciz	"MPI_Graph_get"
	.size	.L__unnamed_86, 14

	.type	.L__unnamed_87,@object  # @86
.L__unnamed_87:
	.asciz	"MPI_Graph_map"
	.size	.L__unnamed_87, 14

	.type	.L__unnamed_88,@object  # @87
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_88:
	.asciz	"MPI_Graph_neighbors"
	.size	.L__unnamed_88, 20

	.type	.L__unnamed_89,@object  # @88
	.p2align	4
.L__unnamed_89:
	.asciz	"MPI_Graph_neighbors_count"
	.size	.L__unnamed_89, 26

	.type	.L__unnamed_90,@object  # @89
	.p2align	4
.L__unnamed_90:
	.asciz	"MPI_Graphdims_get"
	.size	.L__unnamed_90, 18

	.type	.L__unnamed_91,@object  # @90
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_91:
	.asciz	"MPI_Topo_test"
	.size	.L__unnamed_91, 14

	.type	.L__unnamed_92,@object  # @91
.L__unnamed_92:
	.asciz	"MPI_Abort"
	.size	.L__unnamed_92, 10

	.type	.L__unnamed_93,@object  # @92
.L__unnamed_93:
	.asciz	"MPI_Error_class"
	.size	.L__unnamed_93, 16

	.type	.L__unnamed_94,@object  # @93
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_94:
	.asciz	"MPI_Errhandler_create"
	.size	.L__unnamed_94, 22

	.type	.L__unnamed_95,@object  # @94
	.p2align	4
.L__unnamed_95:
	.asciz	"MPI_Errhandler_free"
	.size	.L__unnamed_95, 20

	.type	.L__unnamed_96,@object  # @95
	.p2align	4
.L__unnamed_96:
	.asciz	"MPI_Errhandler_get"
	.size	.L__unnamed_96, 19

	.type	.L__unnamed_97,@object  # @96
	.p2align	4
.L__unnamed_97:
	.asciz	"MPI_Error_string"
	.size	.L__unnamed_97, 17

	.type	.L__unnamed_98,@object  # @97
	.p2align	4
.L__unnamed_98:
	.asciz	"MPI_Errhandler_set"
	.size	.L__unnamed_98, 19

	.type	.L__unnamed_99,@object  # @98
	.p2align	4
.L__unnamed_99:
	.asciz	"MPI_Get_processor_name"
	.size	.L__unnamed_99, 23

	.type	.L__unnamed_100,@object # @99
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_100:
	.asciz	"MPI_Wtick"
	.size	.L__unnamed_100, 10

	.type	.L__unnamed_101,@object # @100
.L__unnamed_101:
	.asciz	"MPI_Wtime"
	.size	.L__unnamed_101, 10

	.type	.L__unnamed_102,@object # @101
.L__unnamed_102:
	.asciz	"MPI_Address"
	.size	.L__unnamed_102, 12

	.type	.L__unnamed_103,@object # @102
.L__unnamed_103:
	.asciz	"MPI_Op_create"
	.size	.L__unnamed_103, 14

	.type	.L__unnamed_104,@object # @103
.L__unnamed_104:
	.asciz	"MPI_Op_free"
	.size	.L__unnamed_104, 12

	.type	.L__unnamed_105,@object # @104
.L__unnamed_105:
	.asciz	"MPI_Attr_delete"
	.size	.L__unnamed_105, 16

	.type	.L__unnamed_106,@object # @105
.L__unnamed_106:
	.asciz	"MPI_Attr_get"
	.size	.L__unnamed_106, 13

	.type	.L__unnamed_107,@object # @106
.L__unnamed_107:
	.asciz	"MPI_Attr_put"
	.size	.L__unnamed_107, 13

	.type	.L__unnamed_108,@object # @107
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_108:
	.asciz	"MPI_Buffer_attach"
	.size	.L__unnamed_108, 18

	.type	.L__unnamed_109,@object # @108
	.p2align	4
.L__unnamed_109:
	.asciz	"MPI_Buffer_detach"
	.size	.L__unnamed_109, 18

	.type	.L__unnamed_110,@object # @109
	.p2align	4
.L__unnamed_110:
	.asciz	"MPI_Get_elements"
	.size	.L__unnamed_110, 17

	.type	.L__unnamed_111,@object # @110
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_111:
	.asciz	"MPI_Get_count"
	.size	.L__unnamed_111, 14

	.type	.L__unnamed_112,@object # @111
.L__unnamed_112:
	.asciz	"MPI_Type_commit"
	.size	.L__unnamed_112, 16

	.type	.L__unnamed_113,@object # @112
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_113:
	.asciz	"MPI_Type_contiguous"
	.size	.L__unnamed_113, 20

	.type	.L__unnamed_114,@object # @113
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_114:
	.asciz	"MPI_Type_extent"
	.size	.L__unnamed_114, 16

	.type	.L__unnamed_115,@object # @114
.L__unnamed_115:
	.asciz	"MPI_Type_free"
	.size	.L__unnamed_115, 14

	.type	.L__unnamed_116,@object # @115
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L__unnamed_116:
	.asciz	"MPI_Type_hindexed"
	.size	.L__unnamed_116, 18

	.type	.L__unnamed_117,@object # @116
	.p2align	4
.L__unnamed_117:
	.asciz	"MPI_Type_hvector"
	.size	.L__unnamed_117, 17

	.type	.L__unnamed_118,@object # @117
	.p2align	4
.L__unnamed_118:
	.asciz	"MPI_Type_indexed"
	.size	.L__unnamed_118, 17

	.type	.L__unnamed_119,@object # @118
	.section	.rodata.str1.1,"aMS",@progbits,1
.L__unnamed_119:
	.asciz	"MPI_Type_lb"
	.size	.L__unnamed_119, 12

	.type	.L__unnamed_120,@object # @119
.L__unnamed_120:
	.asciz	"MPI_Type_size"
	.size	.L__unnamed_120, 14

	.type	.L__unnamed_121,@object # @120
.L__unnamed_121:
	.asciz	"MPI_Type_struct"
	.size	.L__unnamed_121, 16

	.type	.L__unnamed_122,@object # @121
.L__unnamed_122:
	.asciz	"MPI_Type_ub"
	.size	.L__unnamed_122, 12

	.type	.L__unnamed_123,@object # @122
.L__unnamed_123:
	.asciz	"MPI_Type_vector"
	.size	.L__unnamed_123, 16

	.type	.L__unnamed_124,@object # @123
.L__unnamed_124:
	.asciz	"MPI_Unpack"
	.size	.L__unnamed_124, 11

	.type	.L__unnamed_125,@object # @124
.L__unnamed_125:
	.asciz	"MPI_Pack"
	.size	.L__unnamed_125, 9

	.type	.L__unnamed_126,@object # @125
.L__unnamed_126:
	.asciz	"MPI_Pack_size"
	.size	.L__unnamed_126, 14


	.ident	"clang version 7.1.0 (https://github.com/flang-compiler/flang-driver.git 984936abdd04b40140c98ba5e273a3c006780612) (https://github.com/flang-compiler/llvm.git 939ad19087ec3c18718b2b6bb7ae40d7945f54d8)"
	.section	".note.GNU-stack","",@progbits
